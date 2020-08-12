from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from authority_list.models import Person, PersonOtherName, PlaceOtherName, Place, Organisation, OrganisationForm, \
    OrganisationFormScale, OrganisationGenderedMembership, Event
from zarah_db_api.fields import ApproximateDateSerializerField


class PersonOtherNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonOtherName
        exclude = ('person', )


class PersonSerializer(WritableNestedModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    other_names = PersonOtherNameSerializer(many=True, required=False)
    is_removable = serializers.SerializerMethodField()

    def get_is_removable(self, obj):
        user = self.context['request'].user
        return user.is_staff or user.is_superuser

    def get_full_name(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)

    class Meta:
        model = Person
        fields = '__all__'


class PlaceOtherNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOtherName
        exclude = ('place', )


class PlaceSerializer(WritableNestedModelSerializer):
    other_names = PlaceOtherNameSerializer(many=True, required=False)
    is_removable = serializers.SerializerMethodField()

    def get_is_removable(self, obj):
        user = self.context['request'].user
        return user.is_staff or user.is_superuser

    class Meta:
        model = Place
        fields = '__all__'


class OrganisationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationForm
        fields = '__all__'


class OrganisationFormScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationFormScale
        fields = '__all__'


class OrganisationGenderedMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationGenderedMembership
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    is_removable = serializers.SerializerMethodField()

    def get_is_removable(self, obj):
        user = self.context['request'].user
        return user.is_staff or user.is_superuser

    def get_full_name(self, obj):
        if obj.acronym:
            return "%s (%s)" % (obj.name, obj.acronym)
        else:
            return obj.name

    class Meta:
        model = Organisation
        fields = '__all__'


class EventSerializer(WritableNestedModelSerializer):
    date_from = ApproximateDateSerializerField()
    date_to = ApproximateDateSerializerField(required=False)
    is_removable = serializers.SerializerMethodField()

    def get_is_removable(self, obj):
        user = self.context['request'].user
        return user.is_staff or user.is_superuser

    class Meta:
        model = Event
        fields = ('id', 'date_from', 'date_to', 'event', 'event_full', 'is_removable')
