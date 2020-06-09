from django.db import models


# People
class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)

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
    notes = models.TextField(blank=True, null=True)

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


# Places
class Place(models.Model):
    place_name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'places'


class PlaceOtherName(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='other_names')
    place_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'place_other_names'
