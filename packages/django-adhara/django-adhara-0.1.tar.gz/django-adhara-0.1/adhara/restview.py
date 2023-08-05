from itertools import chain

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import ForeignKey
from django.db.models.fields import DateTimeField
from django.db import utils as django_utils
from django.forms.models import model_to_dict
from django.views.generic import View

from .models.base_models import fill_ref_models
from .response_utils import ApiResponse
from .session import Session
from enum import Enum
from .exceptions import InvalidInput


class _Constants(Enum):
    INPUT_META = "_meta"
    META_PAGE = "page"
    PAGE_START = "start"
    PAGE_LENGTH = "length"
    TOTAL_COUNT = "total_count"
    PAGE_CURRENT = "current"
    PAGE_PREVIOUS = "previous"
    PAGE_NEXT = "next"


class RestView(View):
    """
    Rest view to handle API responses in a REST Pattern.
    _meta pattern for get_list
    _meta : {
        "page": {
            "start" : "1",
            "end": "10"
        }
    }
    """
    response_modes_api = "api"
    response_modes_dict = "dict"
    invalid_id = "invalid id"

    def __init__(self, request, model, response_mode="api"):
        self.request = request
        self.db = Session.get_db(request)
        try:
            self.PK = request.PRIMARY_KEY
        except AttributeError:
            self.PK = None
        self.INPUT_JSON = request.INPUT_JSON
        self.INPUT_JSON['request'] = self.request
        if 'id' in self.INPUT_JSON:
            del self.INPUT_JSON['id']
        self.model = model
        self.response_mode = None
        self.set_response_mode(response_mode)
        self.custom_criteria = {}
        self.exclude_criteria = {}
        self.order_by = None
        self.limits = {
            _Constants.PAGE_START.value: 1,
            _Constants.PAGE_LENGTH.value: 100
        }
        self.meta = None
        super(RestView, self).__init__()

    def set_response_mode(self, response_mode):
        self.response_mode = response_mode

    def get_query_criteria(self):
        return self.custom_criteria

    def set_custom_criteria(self, criteria):
        self.custom_criteria = criteria if criteria else self.custom_criteria

    def set_exclude_criteria(self, criteria):
        self.exclude_criteria = criteria

    def set_order_by(self, *order_by):
        self.order_by = order_by

    def get_object(self, criteria=None, *fields):
        if not criteria:
            criteria = {}
        criteria.update(self.get_query_criteria())
        if self.PK:
            criteria['pk'] = self.PK
        try:
            if len(fields):
                return self.model.objects.values(*fields).using(self.db).get(**criteria)
            else:
                return self.model.objects.using(self.db).get(**criteria)
        except ObjectDoesNotExist:
            return None

    def get_count(self):
        return self.model.objects.using(self.db).filter(**self.get_query_criteria()).count()

    def set_limit(self, start, length=100):
        self.limits = {
            _Constants.PAGE_START.value: start,
            _Constants.PAGE_LENGTH.value: length
        }

    def post(self):
        entry = self.model(**self.INPUT_JSON)
        try:
            entry.save(using=self.db)
        except django_utils.DatabaseError as e:
            return self.respond(e.args[1], False)
        response_dict = model_to_dict(entry)
        self.request.NEW_PRIMARY_KEY = entry.pk
        return self.respond(response_dict, True)

    def model_to_dict(self, instance, fields=None, exclude=None):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            skip_serialization = False
            formatted_val = None
            if type(f) == DateTimeField:
                iso_ts = f.value_from_object(instance)
                formatted_val = iso_ts.strftime('%H:%M %p, %B %d, %Y')
            elif type(f) == ForeignKey:
                skip_serialization = f.model._meta.get_field(f.name).rel.to.Adhara.skip_serialization
                if not skip_serialization:
                    value_object = getattr(instance, f.name)
                    if value_object:
                        formatted_val = {
                            "id": value_object.pk,
                            "display_value": str(value_object)
                        }
                    else:
                        formatted_val = None
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude or skip_serialization:
                continue
            data[f.name] = formatted_val if formatted_val else f.value_from_object(instance)
        return data

    def get(self, criteria=None, *fields):
        entry = self.get_object(criteria, *fields)
        if entry is None:
            return self.respond(RestView.invalid_id, False)
        if type(entry) is dict:
            response_dict = entry
        else:
            response_dict = self.model_to_dict(entry)
        return self.respond(response_dict, True)

    def _get_req_meta(self):
        try:
            return self.request.INPUT_JSON[_Constants.INPUT_META.value]
        except KeyError:
            return None

    def _get_limits(self):
        meta = self._get_req_meta()
        if meta:
            if _Constants.META_PAGE.value not in meta:
                meta = {_Constants.META_PAGE.value: {}}
        else:
            meta = {_Constants.META_PAGE.value: {}}

        if _Constants.PAGE_START.value in meta[_Constants.META_PAGE.value]:
            meta[_Constants.META_PAGE.value][_Constants.PAGE_START.value] \
                = int(meta[_Constants.META_PAGE.value][_Constants.PAGE_START.value])
            if meta[_Constants.META_PAGE.value][_Constants.PAGE_START.value] <= 0:
                if self.response_mode == RestView.response_modes_dict:
                    raise InvalidInput("Start index cannot be less than 1" + str(self.model))
                return self.respond("Start index cannot be less than 1", False)

        if _Constants.PAGE_START.value not in meta[_Constants.META_PAGE.value]:
            meta[_Constants.META_PAGE.value][_Constants.PAGE_START.value] = self.limits[_Constants.PAGE_START.value]

        if _Constants.PAGE_LENGTH.value in meta[_Constants.META_PAGE.value]:
            meta[_Constants.META_PAGE.value][_Constants.PAGE_LENGTH.value] = \
                int(meta[_Constants.META_PAGE.value][_Constants.PAGE_LENGTH.value])
            if meta[_Constants.META_PAGE.value][_Constants.PAGE_LENGTH.value] <= 0:
                if self.response_mode == RestView.response_modes_dict:
                    raise InvalidInput("page length cannot be less than 1" + str(self.model))
                return self.respond("page length cannot be less than 1", False)

        if _Constants.PAGE_LENGTH.value not in meta[_Constants.META_PAGE.value]:
            meta[_Constants.META_PAGE.value][_Constants.PAGE_LENGTH.value] = self.limits[_Constants.PAGE_LENGTH.value]

        curr_start = meta[_Constants.META_PAGE.value][_Constants.PAGE_START.value] - 1
        curr_len = meta[_Constants.META_PAGE.value][_Constants.PAGE_LENGTH.value]
        curr_end = curr_start + curr_len
        return curr_start, curr_len, curr_end

    def get_list(self):
        qs = self.model.objects.using(self.db).exclude(**self.exclude_criteria).filter(**self.get_query_criteria())
        if self.order_by:
            qs = qs.order_by(*self.order_by)
        total_count = len(qs)
        curr_start, curr_len, curr_end = self._get_limits()
        qs = qs[curr_start: curr_end]
        response_dict = [self.model_to_dict(x) for x in qs]
        count = len(response_dict)
        meta = self._get_req_meta()
        if meta:
            updated_len = meta[_Constants.META_PAGE.value][_Constants.PAGE_LENGTH.value]
            if count < curr_len:
                updated_len = count
        else:
            updated_len = curr_len
        self.meta = dict({
            _Constants.TOTAL_COUNT.value: total_count,
            _Constants.META_PAGE.value: {
                _Constants.PAGE_CURRENT.value: {
                    _Constants.PAGE_START.value: curr_start,
                    _Constants.PAGE_LENGTH.value: updated_len
                }
            }
        })
        if curr_end < total_count:
            next_total = total_count - curr_end
            next_len = next_total if next_total < curr_len else curr_len
            self.meta[_Constants.META_PAGE.value][_Constants.PAGE_NEXT.value] = {
                _Constants.PAGE_START.value: curr_end + 1,
                _Constants.PAGE_LENGTH.value: next_len,
            }
        if curr_start != 0:
            prev_len = curr_start if curr_start < curr_len else curr_len
            self.meta[_Constants.META_PAGE.value][_Constants.PAGE_PREVIOUS.value] = {
                _Constants.PAGE_START.value: curr_start - prev_len,
                _Constants.PAGE_LENGTH.value: prev_len,
            }

        return self.respond(response_dict, True)

    def _put(self, entry):
        self.INPUT_JSON = fill_ref_models(entry, **self.INPUT_JSON)
        for key, value in self.INPUT_JSON.items():
            setattr(entry, key, value)
        try:
            entry.save()
        except django_utils.DatabaseError as e:
            return self.respond(e.args[1], False)
        response_dict = self.model_to_dict(entry)
        return self.respond(response_dict, True)

    @transaction.atomic
    def put(self, criteria=None):
        entry = self.get_object(criteria)
        if entry is None:
            return self.respond("Does not exist", False)
        return self._put(entry)

    @transaction.atomic
    def put_or_create(self):
        entry = self.get_object()
        if entry is None:
            return self.post()
        return self._put(entry)

    def delete(self):
        try:
            if self.PK:
                self.model.objects.using(self.db).filter(pk=self.PK, **self.get_query_criteria()).delete()
            else:
                self.model.objects.using(self.db).filter(**self.get_query_criteria()).delete()
            return self.respond("Deleted Successfully", True)
        except django_utils.DatabaseError as e:
            return self.respond(e.args[1], False)

    def execute(self):
        if self.request.method == "GET" and not hasattr(self.request, "PRIMARY_KEY"):
            return self.get_list()
        else:
            return getattr(self, self.request.method.lower())()

    def respond(self, data, success):
        return self.get_response(data, success, self.response_mode)

    def get_response(self, data, success, mode="api"):
        if mode == 'api':
            if success:
                return ApiResponse.success(data, self.meta)
            else:
                return ApiResponse.error(data)
        else:
            if success:
                return data
            else:
                raise ValueError(data)
