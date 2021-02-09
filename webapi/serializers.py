from rest_framework import serializers

from authority_list.models import Person, Organisation, Place, Event
from document.models import Document, DocumentTriggeringFactorKeyword, DocumentKeyword, DocumentFile
from metadata.models import Classification


class PlaceSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return "%s (%s)" % (obj.place_name, obj.country)

    class Meta:
        model = Place
        fields = ['full_name']


class OrganisationSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return "%s (%s)" % (obj.name, obj.acronym)

    class Meta:
        model = Organisation
        fields = ['full_name']


class ClassificationSerializer(serializers.ModelSerializer):
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
        fields = ('category_key', 'full_name', 'field_type', 'text')


class DocumentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = ('id', 'file_id', 'file_url')


class DocumentReadPublicSerializer(serializers.ModelSerializer):
    people = serializers.SlugRelatedField(many=True, slug_field='full_name', queryset=Person.objects.all())
    places = PlaceSerializer(many=True, read_only=True)
    organisations = OrganisationSerializer(many=True, read_only=True)
    events = serializers.SlugRelatedField(many=True, slug_field='event_full', queryset=Event.objects.all())
    classifications = serializers.SerializerMethodField()
    keywords = serializers.SlugRelatedField(many=True, slug_field='keyword',
                                            queryset=DocumentKeyword.objects.all())
    triggering_factor_keywords = serializers.SlugRelatedField(many=True, slug_field='keyword',
                                                              queryset=DocumentTriggeringFactorKeyword.objects.all())
    files = DocumentFileSerializer(many=True)

    def get_classifications(self, obj):
        allowed_keys = [
            'historical_context', 'labour_conditions', 'living_conditions', 'labour_relations', 'activist_repertoire',
            'activist_repertoire_scale', 'format_of_participation', 'knowledge_production', 'agendas',
            'effects_of_activism'
        ]
        classifications = Classification.objects.filter(
            document=obj, classification_field__category__key__in=allowed_keys
        )
        serializer = ClassificationSerializer(instance=classifications, many=True)
        return serializer.data

    class Meta:
        model = Document
        exclude = ('summary', 'additional_research')


class DocumentReadTeamSerializer(serializers.ModelSerializer):
    classifications = serializers.SerializerMethodField()
    files = DocumentFileSerializer(many=True)

    def get_classifications(self, obj):
        allowed_keys = ['historical_context']
        classifications = Classification.objects.filter(
            document=obj, classification_field__category__key__in=allowed_keys
        )
        serializer = ClassificationSerializer(instance=classifications, many=True)
        return serializer.data

    class Meta:
        model = Document
        exclude = ('abstract', 'summary', 'additional_research', 'people', 'organisations', 'places', 'events')


class DocumentReadIndividualSerializer(serializers.ModelSerializer):
    files = DocumentFileSerializer(many=True)

    class Meta:
        model = Document
        exclude = ('abstract', 'summary', 'additional_research', 'people', 'organisations', 'places', 'events')