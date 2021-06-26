from django.conf import settings
from django.db import models


# People
from django_date_extensions.fields import ApproximateDateField


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)

    is_public = models.BooleanField(default=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return "%s, %s" % (self.last_name, self.first_name)

    class Meta:
        db_table = 'people'


class PersonOtherName(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='other_names')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'people_other_names'


# Organisations
class Organisation(models.Model):
    name = models.CharField(max_length=300)
    acronym = models.CharField(max_length=50, blank=True)
    organisation_form = models.ForeignKey('OrganisationForm', on_delete=models.PROTECT, blank=True, null=True)
    organisation_form_text = models.TextField(blank=True)
    organisation_form_scale = models.ForeignKey('OrganisationFormScale', on_delete=models.PROTECT, blank=True, null=True)
    organisation_form_scale_text = models.TextField(blank=True)
    organisation_gendered_membership = models.ForeignKey('OrganisationGenderedMembership', on_delete=models.PROTECT, blank=True, null=True)
    organisation_gendered_membership_text = models.TextField(blank=True)
    notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)

    is_public = models.BooleanField(default=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        if self.acronym:
            return "%s (%s)" % (self.name, self.acronym)
        else:
            return self.name

    class Meta:
        db_table = 'organisations'


class OrganisationForm(models.Model):
    form = models.CharField(max_length=100)

    def __str__(self):
        return self.form

    class Meta:
        db_table = 'organisation_forms'


class OrganisationFormScale(models.Model):
    scale = models.CharField(max_length=100)

    class Meta:
        db_table = 'organisation_form_scales'


class OrganisationGenderedMembership(models.Model):
    membership = models.CharField(max_length=100)

    class Meta:
        db_table = 'organisation_gendered_memberships'


# Places
class Place(models.Model):
    place_name = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)

    is_public = models.BooleanField(default=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def place_full(self):
        if self.place_name:
            if self.country:
                return "%s, %s" % (self.place_name, self.country)
            else:
                return self.place_name
        else:
            return self.country

    class Meta:
        db_table = 'places'


class PlaceOtherName(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='other_names')
    place_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'place_other_names'


# Dates
class Event(models.Model):
    date_from = ApproximateDateField()
    date_to = ApproximateDateField(blank=True)
    event = models.CharField(max_length=500, blank=True)
    internal_notes = models.TextField(blank=True, null=True)

    is_public = models.BooleanField(default=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def event_full(self):
        if self.date_to:
            value = "%s - %s" % (self.date_from, self.date_to)
        else:
            value = self.date_from
        return "%s (%s)" % (value, self.event)

    class Meta:
        db_table = 'events'
        ordering = ['date_from', 'date_to', 'event']
