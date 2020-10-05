from rest_framework import generics, filters

from authority_list.models import Person, Place, OrganisationForm, OrganisationFormScale, Organisation, \
    OrganisationGenderedMembership, Event
from authority_list.serializers import PersonSerializer, PlaceSerializer, OrganisationFormSerializer, \
    OrganisationFormScaleSerializer, OrganisationSerializer, OrganisationGenderedMembershipSerializer, EventSerializer


class PersonList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = Person.objects.all().order_by('last_name', 'first_name')
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['last_name', 'first_name']
    search_fields = ['first_name', 'last_name', 'other_names__first_name', 'other_names__last_name']


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PlaceList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = Place.objects.all().order_by('place_name')
    serializer_class = PlaceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_filter = ['place_name', 'country']
    search_fields = ['place_name', 'other_names__place_name']


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class OrganisationGenderedMembershipList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = OrganisationGenderedMembership.objects.all()
    serializer_class = OrganisationGenderedMembershipSerializer


class OrganisationFormList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = OrganisationForm.objects.all()
    serializer_class = OrganisationFormSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['form']


class OrganisationFormScaleList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = OrganisationFormScale.objects.all()
    serializer_class = OrganisationFormScaleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['scale']


class OrganisationList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = Organisation.objects.all().order_by('name', 'acronym')
    serializer_class = OrganisationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'acronym']
    search_fields = ['name', 'acronym']


class OrganisationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class EventList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = Event.objects.all().order_by('date_from', 'event')
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['event', 'date_from', 'date_to']
    search_fields = ['event', 'date_from', 'date_to']


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
