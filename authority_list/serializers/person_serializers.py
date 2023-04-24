from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from authority_list.models import PersonOtherName, Person
from document.models import Document


class PersonOtherNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonOtherName
        exclude = ('person', )


class PersonSerializer(WritableNestedModelSerializer):
    other_names = PersonOtherNameSerializer(many=True, required=False)
    is_removable = serializers.SerializerMethodField()
    is_public = serializers.BooleanField()
    used = serializers.SerializerMethodField()

    def get_is_removable(self, obj):
        user = self.context['request'].user
        return user.is_staff or user.is_superuser

    def get_used(self, obj):
        return Document.objects.filter(people=obj).count()

    class Meta:
        model = Person
        fields = ['id', 'full_name', 'first_name', 'last_name', 'other_names', 'notes', 'internal_notes',
                  'is_removable', 'is_public', 'used', 'created_by']


class PersonAdminSerializer(PersonSerializer):
    is_public = serializers.BooleanField()

    class Meta:
        model = Person
        fields = ['id', 'full_name', 'first_name', 'last_name', 'other_names', 'notes', 'internal_notes',
                  'is_removable', 'is_public', 'used', 'created_by']