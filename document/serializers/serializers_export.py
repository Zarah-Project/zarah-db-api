import json
from django.contrib.auth.models import User

from rest_framework import serializers

from authority_list.models import Organisation, Event, Person, Place, OrganisationForm, OrganisationFormScale, \
    OrganisationGenderedMembership
from document.models import Document, DocumentKeyword, DocumentFile
from metadata.models import DocumentConsent, ConsentType, Classification, ClassificationFurtherExplanation, \
    ClassificationCategory


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
    organisation_form = OrganisationFormSerializer()
    organisation_form_scale = OrganisationFormScaleSerializer()
    organisation_gendered_membership = OrganisationGenderedMembershipSerializer()

    class Meta:
        model = Organisation
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class ClassificationSerializer(serializers.ModelSerializer):
    category_key = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    text = serializers.CharField(source='classification_other_text')

    def get_category_key(self, obj):
        return obj.classification_field.category.key

    def get_full_name(self, obj):
        return obj.classification_field.full_name

    class Meta:
        model = Classification
        fields = ('id', 'category_key', 'full_name', 'text')


class ClassificationFurtherExplanationSerializer(serializers.ModelSerializer):
    category_key = serializers.SlugRelatedField(
        queryset=ClassificationCategory.objects.all(),
        slug_field='key',
        source='category'
    )

    class Meta:
        model = ClassificationFurtherExplanation
        fields = ('id', 'category_key', 'explanation')


class DocumentConsentSerializer(serializers.ModelSerializer):
    consent_type = serializers.SlugRelatedField(queryset=ConsentType.objects.all(), slug_field='key')

    class Meta:
        model = DocumentConsent
        fields = ('id', 'consent_type', 'consent', 'consent_text')


class DocumentKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentKeyword
        fields = ('id', 'keyword')


class DocumentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = ('id', 'file_id', 'file_url')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class DocumentExportSerializer(serializers.ModelSerializer):
    consents = DocumentConsentSerializer(many=True, required=False)
    keywords = DocumentKeywordSerializer(many=True, required=False)
    people = PeopleSerializer(many=True, required=False, read_only=True)
    places = PlaceSerializer(many=True, required=False, read_only=True)
    organisations = OrganisationSerializer(many=True, required=False, read_only=True)
    events = EventSerializer(many=True, required=False, read_only=True)
    classifications = ClassificationSerializer(many=True, required=False, read_only=True)
    explanations = ClassificationFurtherExplanationSerializer(many=True, required=False)
    files = DocumentFileSerializer(many=True, required=False)
    zotero_data = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)

    def get_zotero_data(self, obj):
        return "" if not obj.zotero_data else json.loads(obj.zotero_data)

    class Meta:
        model = Document
        fields = '__all__'
