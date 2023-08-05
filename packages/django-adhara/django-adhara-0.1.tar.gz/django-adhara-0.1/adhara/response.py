from itertools import chain
from django.db.models import ForeignKey
from django.db.models.fields import DateTimeField
from enum import Enum
from .response_utils import ApiResponse


class ResponseModes(Enum):

    JSON = "json"
    MSG_PACK = "msg_pack"


class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    FAILURE = "failure"


class AdharaResponse:

    def __init__(self, adhara_request):
        self.request = adhara_request
        self._response_data = None
        self._status = None

    def success(self, data):
        self._response_data = data
        self._status = ResponseStatus.SUCCESS

    def error(self, data):
        self._response_data = data
        self._status = ResponseStatus.ERROR

    def failure(self, data):
        self._response_data = data
        self._status = ResponseStatus.FAILURE

    def get_response_status(self):
        return self._status

    def _get_response_meta(self):
        return self.request.get_meta().to_dict()

    @staticmethod
    def transform_data(instance, fields=None, exclude=None, transformer=None):
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
        if transformer:
            transformer(instance, data)
        return data

    def get_data(self):
        return self._response_data

    def get_transformed_data(self, transformer=None):
        # TODO integrate with model to dict
        if type(self.get_data()) == list:
            return [AdharaResponse.transform_data(x, transformer) for x in self.get_data()]
        return AdharaResponse.transform_data(self.get_data(), transformer)

    def get_response(self, transformer=None):
        response = {
            "data": self.get_transformed_data(transformer),
            "status": self._status.value
        }
        meta = self._get_response_meta()
        if meta:
            response["meta"] = meta
        return response

    def serialize(self, response_mode=ResponseModes.JSON, transformer=None):
        if response_mode == ResponseModes.JSON:
            if self._status == ResponseStatus.FAILURE:
                return ApiResponse.AsiddhauPratikriyaa(self.get_response(transformer))
            elif self._status == ResponseStatus.ERROR:
                return ApiResponse.SkhalitaPratikriyaa(self.get_response(transformer))
            else:
                return ApiResponse.Pratikriyaa(self.get_response(transformer))
