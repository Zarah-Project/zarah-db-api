from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from authority_list.models import PlaceOtherName, Place
from document.models import Document


class PlaceOtherNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOtherName
        exclude = ('place', )


class PlaceSerializer(WritableNestedModelSerializer):
    other_names = PlaceOtherNameSerializer(many=True, required=False)
    is_removable = serializers.SerializerMethodField()
    is_public = serializers.BooleanField()
    used = serializers.SerializerMethodField()

    def get_is_removable(self, obj):
        user = self.context['request'].user
        return user.is_staff or user.is_superuser

    def get_used(self, obj):
        return Document.objects.filter(places=obj).count()

    class Meta:
        model = Place
        fields = ('id', 'place_name', 'country', 'place_full', 'other_names', 'notes', 'internal_notes', 'is_removable',
                  'is_public', 'used')


class PlaceAdminSerializer(PlaceSerializer):
    is_public = serializers.BooleanField()

    class Meta:
        model = Place
        fields = ('id', 'place_name', 'country', 'place_full', 'other_names', 'notes', 'internal_notes', 'is_removable',
                  'is_public', 'used')
