"""
This file is part of the DSYNC Python SDK package.

(c) DSYNC <support@dsync.com>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""
import hashlib
from datetime import datetime


def generate_entity_token(entity_name):
    """Generate entity token using the name and current time"""
    entity_name = entity_name.replace(' ', '').lower()
    now = datetime.now()
    uuid = hashlib.md5()
    uuid.update('{0}'.format(now.microsecond).encode('utf-8'))
    return 'python-sdk-{0}-{1}'.format(entity_name, uuid.hexdigest())


class ValidationException(Exception):
    """This is thrown by the generate call on an invalid object"""
    pass


class Field:
    """ Filed Object"""
    TYPE_TEXT = 'text'
    TYPE_NUMBER = 'number'
    TYPE_URL = 'url'
    TYPE_EMAIL = 'email'
    TYPE_DATE = 'date'
    TYPE_TIME = 'time'
    TYPE_DATETIME = 'datetime'
    TYPE_BOOLEAN = 'boolean'
    TYPE_OBJECT = 'object'
    TYPE_MATH = 'math'
    TYPE_CUSTOM = 'custom'

    def __init__(self, attributes={}):
        """Initialize field object"""
        self.id = attributes.get('id')
        self.treekey = attributes.get('treekey')
        self.value = attributes.get('value')
        self.type = attributes.get('type')
        self.multiple = attributes.get('multiple', False)
        self.date_format = attributes.get('date_format')
        self.required = attributes.get('required', False)
        self.functions = attributes.get('functions', [])
        self.primary_key = attributes.get('primary_key', False)
        self.foreign_key = attributes.get('foreign_key')
        self.bool_settings = attributes.get('bool_settings')
        self.name = attributes.get('name')
        self.description = attributes.get('description')

    def generate(self):
        """Generate vanilla field object"""
        self.validate()

        return {
            'id': self.id,
            'treekey': self.treekey,
            'value': self.value,
            'type': self.type,
            'multiple': self.multiple,
            'date_format': self.date_format,
            'required': self.required,
            'functions': self.functions,
            'primary_key': self.primary_key,
            'foreign_key': self.foreign_key,
            'bool_settings': self.bool_settings,
            'name': self.name,
            'description': self.description
        }

    def validate(self):
        """Validate before generate vanilla object"""
        error = ''

        if not self.treekey:
            error += 'Treekey is required for this field.'
        if not self.type:
            error += 'Field type is required. '
        if not self.name:
            error += 'Name of field is required. '

        if error:
            raise ValidationException(error)


class Endpoint:
    """Endpoint object"""

    def __init__(self, attributes = {}):
        self.entity_name = attributes.get('entity_name')
        self.treekey = attributes.get('treekey')
        self.endpoint_url = attributes.get('endpoint_url')
        self.entity_token = attributes.get('entity_token')
        self.fields = []

    def add_field(self, field):
        """Add new field to endpoint"""
        self.fields.append(field)

    def add_fields(self, fields):
        """Add multiple fields to endpoint"""
        self.fields.extend(fields)

    def generate(self):
        """Generate vanilla object from endpoint"""
        self.validate()

        return {
            'entity_name': self.entity_name,
            'treekey': self.treekey,
            'endpoint_url': self.endpoint_url,
            'entity_token': self.entity_token,
            'fields': [field.generate() for field in self.fields]
        }

    def validate(self):
        """Validate endpoint object"""
        error = ''

        if not self.treekey:
            error += 'Treekey is required for this endpoint. '

        if not self.entity_name:
            error += 'Entity name is required. '

        if not self.endpoint_url:
            error += 'The endpoint url is required. '

        if not self.entity_token:
            error += 'The entity token is required. '

        if error:
            raise ValidationException(error)


class DataLayout:
    """Data layout object"""

    def __init__(self):
        self.endpoints = []

    def add_endpoint(self, endpoint):
        """Add endpoint to the data layout"""
        self.endpoints.append(endpoint)

    def add_endpoints(self, endpoints):
        """Add multiple endpoints to the data layout"""
        self.endpoints.extend(endpoints)

    def generate(self):
        """Generate vanilla object from data layout"""
        return {
            'data_layout': [endpoint.generate() for endpoint in self.endpoints]
        }

