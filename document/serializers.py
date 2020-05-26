from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from authority_list.models import Organisation, Place, Person
from document.models import Document, DocumentFile, DocumentTriggeringFactorKeyword, DocumentKeyword, DocumentDate
from metadata.models import DocumentConsent, ClassificationFurtherExplanation, ClassificationCategory, Classification, \
    ConsentType
from zarah_db_api.fields import ApproximateDateSerializerField


class DocumentDateSerializer(serializers.ModelSerializer):
    date_from = ApproximateDateSerializerField()
    date_to = ApproximateDateSerializerField(required=False, allow_null=True)

    class Meta:
        model = DocumentDate
        fields = ('id', 'date_from', 'date_to', 'event')


class DocumentKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentKeyword
        fields = ('id', 'keyword')


class DocumentTriggeringFactorKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTriggeringFactorKeyword
        fields = ('id', 'keyword')


class DocumentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = ('id', 'file_id', 'file_url')


class DocumentConsentSerializer(serializers.ModelSerializer):
    consent_type = serializers.SlugRelatedField(queryset=ConsentType.objects.all(), slug_field='key')

    class Meta:
        model = DocumentConsent
        fields = ('id', 'consent_type', 'consent')


class ClassificationFurtherExplanationSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=ClassificationCategory.objects.all(), slug_field='key')

    class Meta:
        model = ClassificationFurtherExplanation
        fields = ('id', 'category', 'explanation')


class OrganisationReadSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='pk', read_only=True)
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        if obj.acronym:
            return "%s (%s)" % (obj.name, obj.acronym)
        else:
            return obj.name

    class Meta:
        model = Organisation
        fields = ('value', 'label')


class PeopleReadSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='pk', read_only=True)
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)

    class Meta:
        model = Person
        fields = ('value', 'label')


class PlaceReadSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='pk', read_only=True)
    label = serializers.CharField(source='place_name', read_only=True)

    class Meta:
        model = Place
        fields = ('value', 'label')


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = ('id', 'classification_field', 'classification_other_text')


class ClassificationReadSerializer(serializers.ModelSerializer):
    field_id = serializers.SerializerMethodField()
    category_key = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    field_type = serializers.SerializerMethodField()
    text = serializers.CharField(source='classification_other_text')

    def get_category_key(self, obj):
        return obj.classification_field.category.key

    def get_full_name(self, obj):
        return obj.classification_field.full_name

    def get_field_type(self, obj):
        return obj.classification_field.field_type

    def get_field_id(self, obj):
        return obj.classification_field.id

    class Meta:
        model = Classification
        fields = ('id', 'category_key', 'full_name', 'field_type', 'text', 'field_id')


class DocumentReadSerializer(serializers.ModelSerializer):
    consents = DocumentConsentSerializer(many=True, required=False)
    dates = DocumentDateSerializer(many=True, required=False)
    keywords = DocumentKeywordSerializer(many=True, required=False)
    people = PeopleReadSerializer(many=True, required=False, read_only=True)
    places = PlaceReadSerializer(many=True, required=False, read_only=True)
    organisations = OrganisationReadSerializer(many=True, required=False, read_only=True)
    classifications = ClassificationReadSerializer(many=True, required=False, read_only=True)
    explanations = ClassificationFurtherExplanationSerializer(many=True, required=False)
    files = DocumentFileSerializer(many=True, required=False)

    class Meta:
        model = Document
        fields = '__all__'


class DocumentWriteSerializer(WritableNestedModelSerializer):
    consents = DocumentConsentSerializer(many=True, required=False)
    dates = DocumentDateSerializer(many=True, required=False)
    keywords = DocumentKeywordSerializer(many=True, required=False)
    triggering_factor_keywords = DocumentTriggeringFactorKeywordSerializer(many=True, required=False)
    files = DocumentFileSerializer(many=True, required=False)
    classifications = ClassificationSerializer(many=True, required=False)
    explanations = ClassificationFurtherExplanationSerializer(many=True, required=False)

    class Meta:
        model = Document
        fields = '__all__'
