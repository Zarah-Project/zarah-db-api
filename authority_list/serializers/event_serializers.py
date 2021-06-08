from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from authority_list.models import Event
from document.models import Document
from zarah_db_api.fields import ApproximateDateSerializerField


class EventSerializer(WritableNestedModelSerializer):
    date_from = ApproximateDateSerializerField()
    date_to = ApproximateDateSerializerField(required=False)
    is_removable = serializers.SerializerMethodField()
    is_public_user = serializers.BooleanField(read_only=True, source='is_public')
    used = serializers.SerializerMethodField()

    def get_is_removable(self, obj):
        user = self.context['request'].user
        return user.is_staff or user.is_superuser

    def get_used(self, obj):
        return Document.objects.filter(events=obj).count()

    class Meta:
        model = Event
        fields = ('id', 'date_from', 'date_to', 'event', 'event_full', 'internal_notes', 'used', 'is_removable',
                  'is_public_user', 'created_by')


class EventAdminSerializer(EventSerializer):
    is_public = serializers.BooleanField()

    class Meta:
        model = Event
        fields = ('id', 'date_from', 'date_to', 'event', 'event_full', 'internal_notes', 'used', 'is_removable',
                  'is_public', 'created_by')
