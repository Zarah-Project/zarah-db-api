from django.conf import settings
from pyzotero import zotero
from rest_framework import serializers

from authority_list.models import Person, Organisation, Place, Event, PersonOtherName, PlaceOtherName, OrganisationForm, \
    OrganisationFormScale
from authority_list.serializers.person_serializers import PersonOtherNameSerializer
from authority_list.serializers.place_serializers import PlaceOtherNameSerializer
from document.models import Document, DocumentTriggeringFactorKeyword, DocumentKeyword, DocumentFile
from metadata.models import Classification


class PersonSerializer(serializers.ModelSerializer):
    other_names = PersonOtherNameSerializer(many=True, required=False)

    class Meta:
        model = Person
        fields = ['id', 'full_name', 'other_names', 'notes']


class PlaceSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    other_names = PlaceOtherNameSerializer(many=True, required=False)

    def get_full_name(self, obj):
        on = []
        for other_name in obj.other_names.iterator():
            on.append(other_name.place_name.strip())

        if len(on) > 0:
            places = "%s/%s" % (obj.place_name, "/".join(on))
        else:
            places = obj.place_name

        if obj.country:
            return "%s (%s)" % (places, obj.country)
        else:
            return places

    class Meta:
        model = Place
        fields = ['id', 'full_name', 'place_full', 'place_name', 'other_names', 'country', 'notes']


class OrganisationSerializer(serializers.ModelSerializer):
    organisation_form = serializers.SlugRelatedField(slug_field='form', queryset=OrganisationForm.objects.all())
    organisation_form_scale = serializers.SlugRelatedField(slug_field='scale', queryset=OrganisationFormScale.objects.all())
    organisation_gendered_membership = serializers.SlugRelatedField(slug_field='membership', queryset=OrganisationFormScale.objects.all())

    class Meta:
        model = Organisation
        fields = ['id', 'full_name', 'name', 'acronym',
                  'organisation_form', 'organisation_form_text',
                  'organisation_form_scale', 'organisation_form_scale_text',
                  'organisation_gendered_membership', 'organisation_gendered_membership_text',
                  'notes']


class EventSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        if obj.date_to:
            return "%s - %s" % (obj.date_from, obj.date_to)
        else:
            return str(obj.date_from)

    class Meta:
        model = Event
        fields = ['event_full', 'date', 'event']


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
    people = PersonSerializer(many=True, read_only=True)
    places = PlaceSerializer(many=True, read_only=True)
    organisations = OrganisationSerializer(many=True, read_only=True)
    events = EventSerializer(many=True, read_only=True)
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


class DocumentCitationSerializer(serializers.ModelSerializer):
    citation = serializers.SerializerMethodField()

    def get_citation(self, obj):
        zotero_id = obj.zotero_id
        if zotero_id:
            zot = zotero.Zotero(settings.ZOTERO_LIBRARY_ID, 'group', settings.ZOTERO_API_KEY)
            zot.add_parameters(content='bib')
            item = zot.item(zotero_id)
            return item[0].replace('</div>', ' Retrieved from ZARAH DB database.</div>')

    class Meta:
        model = Document
        fields = ('citation',)