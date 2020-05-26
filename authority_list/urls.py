from django.urls import path

from authority_list.views import PersonList, PersonDetail, PlaceList, PlaceDetail, OrganisationList, OrganisationDetail, \
    OrganisationFormList, OrganisationFormScaleList

app_name = 'authority_list'

urlpatterns = [
    # Organisations
    path('organisations/', OrganisationList.as_view(), name='organisation-list'),
    path('organisations/<int:pk>/', OrganisationDetail.as_view(), name='organisation-detail'),

    path('organisation_forms/', OrganisationFormList.as_view(), name='organisation-form-list'),
    path('organisation_form_scales/', OrganisationFormScaleList.as_view(), name='organisation-form-scale-list'),

    # People
    path('people/', PersonList.as_view(), name='person-list'),
    path('people/<int:pk>/', PersonDetail.as_view(), name='person-detail'),

    # Place
    path('places/', PlaceList.as_view(), name='place-list'),
    path('places/<int:pk>/', PlaceDetail.as_view(), name='place-detail'),
]