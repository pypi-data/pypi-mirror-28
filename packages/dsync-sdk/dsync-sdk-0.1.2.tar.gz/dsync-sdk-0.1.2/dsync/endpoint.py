# -*- coding: utf-8 -*-
"""
 This file is part of the DSYNC Python SDK package.

(c) DSYNC <support@dsync.com>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""
import sys
from .http import Client, Request
from .http import HTTP_GET, HTTP_PUT, HTTP_DELETE, HTTP_POST

DEFAULT_ENDPOINT = 'https://api.dsync.com/api/realtime'


class RealtimeRequestException(Exception):
    """Real time request exception"""
    pass
    

class RealtimeRequest:
    """Real time request """

    def __init__(self, auth_token=None, entity_token=None, realtime_endpoint=DEFAULT_ENDPOINT):
        """Set authorization token, endpoint token and endpoint"""
        self._auth_token = auth_token
        self._entity_token = entity_token
        self._realtime_endpoint = realtime_endpoint

    def create(self, data):
        """Sends a CREATE entity request to Dsync"""
        self.__request(HTTP_POST, data=data)

    def update(self, data):
        """Sends an UPDATE entity request to Dsync"""
        self.__request(HTTP_PUT, data=data)

    def delete(self, entity_id):
        """Sends a DELETE entity request to Dsync"""
        self.__request(HTTP_DELETE, entity_id=entity_id)

    def __request(self, method, entity_id=None, data=None):
        """Utility method used to send the request"""

        try:
            headers = {
                'Content-Type': 'application/json',
                'Entity-Token': self._entity_token,
                'Auth-Token': self._auth_token
            }

            request = Request(method, headers)

            if entity_id:
                request.add_header('Entity-Id', entity_id)

            if data:
                request.set_body(data)

            client = Client(self._realtime_endpoint)
            result = client.send(request)

            if result.status_code != 200:
                error = 'There was an error making this realtime request.'
                if result.body and result.body.get('message'):
                    error = result.body.get('message')
                raise RealtimeRequestException(error)
        except:
            error = err = sys.exc_info()[0]
            raise RealtimeRequestException(error)

