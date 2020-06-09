from rest_framework import generics, filters

from authority_list.models import Person, Place, OrganisationForm, OrganisationFormScale, Organisation, \
    OrganisationGenderedMembership
from authority_list.serializers import PersonSerializer, PlaceSerializer, OrganisationFormSerializer, \
    OrganisationFormScaleSerializer, OrganisationSerializer, OrganisationGenderedMembershipSerializer


class PersonList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'other_names__first_name', 'other_names__last_name']


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PlaceList(generics.ListCreateAPIView):
    pagination_class = None
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [filters.SearchFilter]
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
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'acronym']


class OrganisationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
