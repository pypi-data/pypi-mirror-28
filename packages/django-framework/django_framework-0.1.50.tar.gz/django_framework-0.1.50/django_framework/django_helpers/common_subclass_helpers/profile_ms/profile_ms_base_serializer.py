from rest_framework import serializers


from django_framework.django_helpers.serializer_helpers import BaseSerializer
from django_framework.django_helpers.serializer_helpers.serialize_registry import register_serializer
from django_framework.django_helpers.serializer_helpers.serialize_registry import get_serializer

from django_framework.django_helpers.serializer_helpers.serializer_fields import ManyToManyIdListField, TripleDesField, UnixEpochDateTimeField
from django_framework.django_helpers.model_helpers.model_registry import get_model
from django.core.exceptions import ValidationError

class ProfileMSBaseSerializer(BaseSerializer):
    
    profile_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        
        model = None
        fields = BaseSerializer.Meta.fields + [
            'profile_id',
        ]
        
        read_only_fields = ["id", "type", "last_updated", "created_at"]  # note that UUID is removed
        hidden_fields = [] # attempting to PUT to it will error.
        write_once_fields = ["id", "type", "uuid", "created_at"] # can only be set upon creation. not editable after
        
