"""
This file is part of the DSYNC Python SDK package.

(c) DSYNC <support@dsync.com>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import requests
import json
import sys

HTTP_GET = 'GET'
HTTP_POST = 'POST'
HTTP_PUT = 'PUT'
HTTP_DELETE = 'DELETE'


class ClientException(Exception):
    """Custom client exception"""
    pass


class Request:
    """Request object, defines the HTTP request"""

    def __init__(self, method=HTTP_GET, headers={}, body=None):
        """Initialize the request object"""
        self.method = method
        self.headers = headers
        self.body = body

    def add_header(self, key, value):
        """Add header to request"""
        self.headers[key] = value

    def set_headers(self, headers):
        """Override request headers"""
        self.headers = headers

    def get_headers(self):
        """Get request headers"""
        return self.headers

    def set_body(self, body):
        """Override request body"""
        self.body = body

    def get_body(self):
        """Get request body"""
        if self.headers.get('Content-Type') == 'application/json':
            return json.dumps(self.body)

        return self.body

    def set_method(self, method):
        """Set request method"""
        self.method = method

    def get_method(self):
        """Get request method"""
        return self.method


class Response:
    """Request response object"""

    def __init__(self, status_code, body):
        """Init response object"""
        self.status_code = status_code
        self.body = body


class Client:
    """HTTP transport layer client (wrapper over requests lib)"""

    def __init__(self, url):
        """Initialize client"""
        self.url = url

    def send(self, request):
        """Send HTTP request"""
        if request.method == HTTP_POST:
            return self._post(request)

        if request.method == HTTP_GET:
            return self._get(request)

        if request.method == HTTP_DELETE:
            return self._delete(request)

        if request.method == HTTP_PUT:
            return self._delete(request)

        raise ClientException('Unknown method: ' + request.method)

    def _post(self, request):
        """Make post request to url"""
        try:
            response = requests.post(self.url, data=request.get_body(), headers=request.get_headers())
            return self._post_request(response)
        except:
            err = sys.exc_info()[0]
            raise ClientException(err.strerror)

    def _delete(self, request):
        """Make delete request to url"""
        try:
            response = requests.delete(self.url, headers=request.get_headers())
            return self._post_request(response)
        except:
            err = sys.exc_info()[0]
            raise ClientException(err.strerror)

    def _put(self, request):
        """Make put request to url"""
        try:
            response = requests.put(self.url, data=request.get_body(), headers=request.get_headers())
            return self._post_request(response)
        except:
            err = sys.exc_info()[0]
            raise ClientException(err.strerror)

    def _get(self, request):
        """Make get request to url"""
        try:
            response = requests.get(self.url, headers=request.get_headers())
            return self._post_request(response)
        except:
            err = sys.exc_info()[0]
            raise ClientException(err.strerror)

    def _post_request(self, response):
        """post request processing"""
        body = response.text
        if response.headers.get('content-type') == 'application/json':
            try:
                body = json.loads(body)
            except:
                raise ClientException('Failed to parse json response' + body)

        return Response(response.status_code, body)

