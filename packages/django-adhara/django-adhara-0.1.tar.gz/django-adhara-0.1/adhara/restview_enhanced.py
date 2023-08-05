from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db import utils as django_utils
from django.forms.models import model_to_dict
from django.views.generic import View

from .models.base_models import fill_ref_models
from .response import AdharaResponse


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

    def __init__(self, adhara_request, model, transformer = None):
        self._request = adhara_request
        self.db = adhara_request.get_tenant_db()
        self.INPUT_JSON = adhara_request.get_input()
        self.model = model
        self._transformer = transformer
        self._response = AdharaResponse(self._request)
        super(RestView, self).__init__()

    def _get_query_criteria(self):
        return self._request.get_criteria_object().get_criteria()

    def _get_exclude_criteria(self):
        return self._request.get_exclude_criteria_object().get_criteria()

    def _get_object(self, *fields):
        criteria = self._request.get_criteria_object().get_criteria()
        try:
            if len(fields):
                return self.model.objects.values(*fields).using(self.db).get(**criteria)
            else:
                return self.model.objects.using(self.db).get(**criteria)
        except ObjectDoesNotExist:
            return None

    def get_count(self):
        self._response.success(self.model.objects.using(self.db).filter(**self._get_query_criteria()).count())
        return self._response

    def post(self):
        with transaction.atomic(using=self.db):
            entry = self.model(**self._request.get_input())
            try:
                entry.save(using=self.db)
            except django_utils.DatabaseError as e:
                return self._response.error(e.args[1])
            response_dict = model_to_dict(entry)
            # self._request.NEW_PRIMARY_KEY = entry.pk    # TODO
        self._response.success(response_dict)
        return self._response

    def get(self, *fields):
        entry = self._get_object(*fields)
        if entry is None:
            return self._response.error("Invalid identifier")
        response_dict = entry
        self._response.success(response_dict)
        return self._response

    def get_list(self):
        qs = self.model.objects.using(self.db)\
            .exclude(**self._get_exclude_criteria())\
            .filter(**self._get_query_criteria())
        order_by = self._request.get_meta().get_order_by()
        if order_by:
            qs = qs.order_by(*order_by)
        total_count = len(qs)
        pagination = self._request.get_meta().get_pagination()
        curr_page = pagination.get_current_page()
        qs = qs[curr_page.get_start(): curr_page.get_end()]
        count = len(qs)
        pagination.update_page_properties(count, total_count)
        self._response.success(qs)
        return self._response

    def _put(self, entry):
        # TODO handle
        filled_input = fill_ref_models(entry, **self._request.get_input())
        for key, value in filled_input.items():
            setattr(entry, key, value)
        try:
            entry.save()
        except django_utils.DatabaseError as e:
            return self._response.error(e.args[1])
        self._response.success(entry)
        return self._response

    def put(self):
        with transaction.atomic(using=self.db):
            entry = self._get_object()
            if entry is None:
                return self._response.error("Does not exist")
            return self._put(entry)

    def put_or_create(self):
        with transaction.atomic(using=self.db):
            entry = self._get_object()
            if entry is None:
                return self.post()
            return self._put(entry)

    def delete(self):
        try:
            identifier = self._request.get_identifier()
            if identifier:
                self.model.objects.using(self.db).filter(pk=identifier, **self._get_query_criteria()).delete()
            else:
                self.model.objects.using(self.db).filter(**self._get_query_criteria()).delete()
            return self._response.success("Deleted Successfully")
        except django_utils.DatabaseError as e:
            self._response.error(e.args[1])
        return self._response

    def execute(self):
        return getattr(self, self._request.get_method().value.lower())()
        # if self._request.get_method() == "GET" and not self._request.get_identifier():
        #     return self.get_list()
        # else:
        #     return getattr(self, self._request.method.lower())()
