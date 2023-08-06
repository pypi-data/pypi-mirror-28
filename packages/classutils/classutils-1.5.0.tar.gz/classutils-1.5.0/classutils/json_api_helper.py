import json
from requests.models import Response
from tableutil import Table

CLASS_NAME = u'class_name'
KEY = u'key'
MANDATORY = u'mandatory'
OPTIONAL = u'optional'
PROPERTY = u'property'
TYPE = u'type'
PROPERTY_NAME = u'property_name'
PROPERTIES = u'properties'
DEFAULT = u'default'
ATTRIBUTES = u'attributes'
FILENAME = u"filename"
MIXIN_IMPORTS = u'mixin_imports'


class MandatoryFieldMissing(Exception):
    pass


class JsonApiRequestResponse(object):

    REQUEST = u'request'
    RESPONSE = u'response'

    def __init__(self,
                 request,
                 response):
        self._request = request
        self._response = response

    @property
    def request(self):
        return self.json()[self.REQUEST]

    @property
    def response(self):
        return self.json()[self.RESPONSE]

    def json(self):
        try:
            json = self._response.json()
        except (AttributeError, ValueError):
            json = self._response

        return {self.REQUEST:  self._request,
                self.RESPONSE: json}


class JsonApiPropertiesClass(object):

    ALLOW_REDIRECTS = False

    def __init__(self,
                 response=None,
                 request=None,
                 parent=None):
        """
        Provides base class for API classes that use properties instead of
        keys into a dictionary.

        It's not mandatory to call __init__. You can explicitly set self.response_dict instead
        if that makes more sense in your subclass

        :param response: One of: None - Expect the request method to be overriden that returns
                                        one of the remaining response types...
                                 requests.models.Response - request has already been made
                                 JSON String - request has been made / this is part of a response
                                               hierarchy.
                                 Dictionary - JSON has already been unpacked. (Don't supply lists)
        :param parent: Can pass the parent object, so that a subclass can access its properties.
                       Useful inside the request method, for example.
        """

        if not request:
            try:
                request = self.get_property(u'_request')
            except ValueError:
                pass  # _request is not in the object tree

        if response is None:
            # No response, must fetch
            response = self.request(request)
            # May have to do something special for web socket requests
            # but for now rely on passing the request

        if isinstance(response, Response):
            self._request = request if request else response.url
            self._response = response
            response = response.json()

        elif isinstance(response, JsonApiRequestResponse):
            self._original_json_api_request_response = response
            self._request = response.request
            self._response = response.response
            response = response.response
        else:
            self._request = request

        try:
            self._response_dict = json.loads(response)
        except:
            self._response_dict = response

        self.parent = parent
        super(JsonApiPropertiesClass, self).__init__()  # Required for co-operative multiple inheritance

    @property
    def request_headers(self):
        return None

    @property
    def request_parameters(self):
        return None

    def request(self,
                request):
        raise NotImplementedError(u'response==None passed for response {cls} '
                                  u'where the request method has not be overridden.'
                                  u'request=={request}'
                                  .format(cls=str(self.__class__),
                                          request=request))

    def mandatory(self,
                  key):
        try:
            return self._response_dict[key]
        except KeyError:
            raise MandatoryFieldMissing(key)

    def optional(self,
                 key,
                 default=None):
        try:
            return self._response_dict.get(key, default)
        except AttributeError:
            raise TypeError(u'API response is not JSON')

    def get_property(self,
                     item):
        try:
            return getattr(self, item)
        except AttributeError:
            pass
        try:
            return getattr(self.parent.item)
        except AttributeError as ae:
            pass
        try:
            return self.parent.get_property(item)
        except AttributeError as ae:
            raise ValueError(u'Could not find "{item}" in object tree'.format(item=item))

    @property
    def _title(self):
        """Override to add a customised title to the table"""
        return self._request

    @property
    def table(self):
        """
        Generates a table from self.response_dict.
        Override if a custom table is required.
        :return: Table instance
        """
        try:
            return self._table
        except:
            pass

        try:
            conversions = self.CONVERSIONS
        except:
            conversions = None

        self._table = Table.init_from_tree(
                tree=self._response_dict,
                title=self._title,
                conversions=conversions)

        return self._table
