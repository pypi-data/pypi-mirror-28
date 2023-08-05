from .session import Session
from .meta import Meta
from enum import Enum


class APIMethods(Enum):
    GET = "GET"
    GET_LIST = "GET_LIST"
    GET_COUNT = "GET_COUNT"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class Criteria:

    def __init__(self, criteria=None, identifier=None):
        self._criteria = criteria or {}
        self._identifier = identifier

    def set_criteria(self, criteria=None):
        self._criteria = criteria or {}

    def get_criteria(self):
        if self._identifier:
            criteria = {"pk": self._identifier}
            criteria.update(self._criteria)
        else:
            criteria = self._criteria
        return criteria

    def update_criteria(self, criteria):
        self._criteria.update(criteria)


class AdharaRequest:

    def __init__(self, request, method=None, input_json=None, identifier=None,
                 meta=None, criteria=None, exclude_criteria=None):
        self._request = request
        self._identifier = identifier
        self._input_json = input_json
        self._identifier = identifier
        self._method = None
        self._set_method_(method)
        self._meta = meta or Meta()
        self._criteria = Criteria(criteria, identifier)
        self._exclude_criteria = Criteria(exclude_criteria)

    def _set_method_(self, method=None):
        query_methods = [APIMethods.GET_LIST, APIMethods.GET]
        if self.get_method() in query_methods or method in query_methods:
            self.set_method(APIMethods.GET if self.get_identifier() else APIMethods.GET_LIST)
        elif method:
            self.set_method(method)

    def get_method(self):
        return self._method

    def set_method(self, method):
        self._method = method

    def get_criteria_object(self):
        return self._criteria

    def get_exclude_criteria_object(self):
        return self._exclude_criteria

    def get_meta(self):
        return self._meta

    def get_input(self):
        required_input = {
            "request": self._request
        }
        if self._input_json:
            required_input.update(self._input_json)
        if 'id' in required_input:
            del required_input['id']
        return required_input

    def get_identifier(self):
        return self._identifier

    def set_identifier(self, identifier=None):
        self._identifier = identifier
        self._set_method_()

    def get_tenant_db(self):
        return Session.get_db(self._request)
