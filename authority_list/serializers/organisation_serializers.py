from rest_framework import serializers

from authority_list.models import OrganisationForm, OrganisationFormScale, OrganisationGenderedMembership, Organisation
from document.models import Document


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
    full_name = serializers.SerializerMethodField()
    is_removable = serializers.SerializerMethodField()
    is_public_user = serializers.BooleanField(read_only=True, source='is_public')
    used = serializers.SerializerMethodField()

    def get_is_removable(self, obj):
        user = self.context['request'].user
        return user.is_staff or user.is_superuser

    def get_full_name(self, obj):
        if obj.acronym:
            return "%s (%s)" % (obj.name, obj.acronym)
        else:
            return obj.name

    def get_used(self, obj):
        return Document.objects.filter(organisations=obj).count()

    class Meta:
        model = Organisation
        fields = '__all__'


class OrganisationAdminSerializer(OrganisationSerializer):
    is_public = serializers.BooleanField(read_only=True)

    class Meta:
        model = Organisation
        fields = '__all__'
