from .domain import DomainEvent
from .schema import get_event_version
from .settings import adds_schema_version_to_event_data
from .utils import camel_case_to_snake_case
from collections import namedtuple
from datetime import datetime
from eventsourcing.domain.model.events import resolve_attr
from eventsourcing.domain.services.transcoding import AbstractTranscoder
from eventsourcing.domain.services.transcoding import ObjectJSONDecoder
from eventsourcing.domain.services.transcoding import id_prefix_from_event
from eventsourcing.domain.services.transcoding import make_stored_entity_id
from eventsourcing.utils.time import timestamp_from_uuid
from inspect import isclass

import importlib
import json


UnifiedStoredEvent = namedtuple('UnifiedStoredEvent', [
    'event_id',
    'event_type',
    'event_version',
    'event_data',
    'aggregate_id',
    'aggregate_type',
    'aggregate_version',
    'create_date',
    'metadata',
    'module_name',
    'class_name',
    'stored_entity_id',
])


class UnifiedTranscoder(AbstractTranscoder):
    def __init__(self, json_encoder_cls=None):
        self.json_encoder_cls = json_encoder_cls
        # encrypt not implemented

    def serialize(self, domain_event):
        """
           Serializes a domain event into a stored event.
        """
        assert isinstance(domain_event, DomainEvent)

        event_data = {key: value for key, value in domain_event.__dict__.items() if key not in {
            'domain_event_id',
            'entity_id',
            'entity_version',
            'metadata',
        }}

        domain_event_class = type(domain_event)
        event_version = get_event_version(domain_event_class)

        return UnifiedStoredEvent(
            event_id=domain_event.domain_event_id,
            event_type=get_event_type(domain_event),
            event_version=event_version,
            event_data=self._json_encode(event_data),
            aggregate_id=domain_event.entity_id,
            aggregate_type=get_aggregate_type(domain_event),
            aggregate_version=domain_event.entity_version,
            create_date=datetime.fromtimestamp(timestamp_from_uuid(domain_event.domain_event_id)),
            metadata=self._json_encode(getattr(domain_event, 'metadata', None)),
            module_name=domain_event_class.__module__,
            class_name=domain_event_class.__qualname__,
            # have to have stored_entity_id because of the lib
            stored_entity_id=make_stored_entity_id(id_prefix_from_event(domain_event), domain_event.entity_id),
        )

    def deserialize(self, stored_event):
        """
        Recreates original domain event from stored event topic and event attrs.
        """
        assert isinstance(stored_event, UnifiedStoredEvent)
        # Get the domain event class from the topic.
        domain_event_class = self._get_domain_event_class(stored_event.module_name, stored_event.class_name)

        # Deserialize event attributes from JSON
        event_attrs = self._json_decode(stored_event.event_data)

        # Reinstantiate and return the domain event object.
        defaults = {
            'entity_id': stored_event.aggregate_id,
            'entity_version': stored_event.aggregate_version,
            'domain_event_id': stored_event.event_id,
        }

        if adds_schema_version_to_event_data():
            defaults['schema_version'] = None

        kwargs = {**defaults, **event_attrs}

        try:
            domain_event = domain_event_class(**kwargs)
        except TypeError:
            raise ValueError("Unable to instantiate class '{}' with data '{}'"
                             "".format(stored_event.class_name, event_attrs))

        return domain_event

    @staticmethod
    def _get_domain_event_class(module_name, class_name):
        """Return domain class described by given topic.

        Args:
            module_name: string of module_name
            class_name: string of class_name
        Returns:
            A domain class.

        Raises:
            ResolveDomainFailed: If there is no such domain class.
        """
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise ResolveDomainFailed("{}#{}: {}".format(module_name, class_name, e))
        try:
            domain_event_class = resolve_attr(module, class_name)
        except AttributeError as e:
            raise ResolveDomainFailed("{}#{}: {}".format(module_name, class_name, e))

        if not isclass(domain_event_class):
            raise ValueError("Event class is not a type: {}".format(domain_event_class))

        if not issubclass(domain_event_class, DomainEvent):
            raise ValueError("Event class is not a DomainEvent: {}".format(domain_event_class))

        return domain_event_class

    def _json_encode(self, data):
        return json.dumps(data, separators=(',', ':'), sort_keys=True, cls=self.json_encoder_cls)

    def _json_decode(self, json_str):
        return json.loads(json_str, cls=ObjectJSONDecoder)


class ResolveDomainFailed(Exception):
    pass


def get_aggregate_type(domain_event):
    assert isinstance(domain_event, DomainEvent)
    domain_event_class = type(domain_event)
    return domain_event_class.__qualname__.split('.')[0]


def get_event_type(domain_event):
    if hasattr(domain_event, 'event_type'):
        return getattr(domain_event, 'event_type')
    else:
        aggregate_type = get_aggregate_type(domain_event)
        event_name = domain_event.__class__.__name__
        event_type_name = '%s%s' % (aggregate_type, event_name)
        return camel_case_to_snake_case(event_type_name)
