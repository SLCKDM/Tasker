from collections import OrderedDict
from typing import Sequence
from django.urls import reverse
from rest_framework import serializers
import django.db.models
from rest_framework.fields import (empty, iter_options)

class ClassNameSerializer(serializers.Field):

    # def get_attribute(self, instance: django.db.models.Model):
    #     return instance

    def to_representation(self, value: django.db.models.Model) -> str:
        return value.__class__.__name__


# TODO: change models inner metadata serialization from
# [{}, {}, {}]
# into
# [{'meta': {}}, {'meta': {}}, {'meta': {}}]
class MetadataField(serializers.Field):

    def __init__(self, *, view_name = None, read_only=True, write_only=False,
                 required=None, default=empty, initial=empty, source=None,
                 label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False):
        self.view_name = view_name
        super().__init__(read_only=read_only, write_only=write_only,
                         required=required, default=default, initial=initial,
                         source=source, label=label, help_text=help_text,
                         style=style, error_messages=error_messages,
                         validators=validators, allow_null=allow_null)


    def get_attribute(self, instance):
        return instance

    def to_representation(self, instance) -> dict:
        # need to pass specific viewname
        request = self.context['request']
        metadata = {
            'url': request.build_absolute_uri(reverse(self.view_name, args=[instance.uuid])),
            'object_type': ClassNameSerializer().to_representation(instance),
            'mediatype': 'application/json',
        }
        return metadata

    def to_internal_value(self, data):
        return super().to_internal_value(data['url'])



class MetadataRelatedField(
    serializers.HyperlinkedRelatedField,
):
    def to_representation(self, instance) -> dict:
        # need to pass specific viewname
        request = self.context['request']
        metadata = {
            'url': request.build_absolute_uri(reverse(self.view_name, args=[instance.uuid])),
            'object_type': ClassNameSerializer().to_representation(instance),
            'mediatype': 'application/json',
        }
        return metadata

    def to_internal_value(self, uuid):
        return super().to_internal_value(data['url'])


    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                self.display_value(item),
                self.to_representation(item),
            )
            for item in queryset
        ])


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:  # ! Здесь поля дропаются не только для вывода, но и для остальных методов, исправить
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def run_validation(self, data=empty):
        return super().run_validation(data)