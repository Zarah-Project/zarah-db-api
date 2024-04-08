from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver

from authority_list.models import Person, Organisation, Place, Event
from authority_list.tasks import remove_authority_record, add_authority_record
from document.models import Document
from document.tasks import index_document_admin, index_document_public, remove_document_admin, remove_document_public


@receiver([post_save], sender=Document)
def do_index(sender, instance, **kwargs):
    index_document_admin(instance.id)
    index_document_public.delay(instance.id)


@receiver([pre_delete], sender=Document)
def remove_index(sender, instance, **kwargs):
    remove_document_admin(instance.id)
    remove_document_public.delay(instance.id)


@receiver([m2m_changed], sender=Document.people.through)
def update_person_index(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            add_authority_record.delay(pk, 'person')
    if action == 'post_remove':
        for pk in pk_set:
            person = Person.objects.get(pk=pk)
            if Document.objects.filter(people__in=[person]).count() == 0:
                remove_authority_record.delay(pk, 'person')


@receiver([m2m_changed], sender=Document.organisations.through)
def update_organisation_index(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            add_authority_record.delay(pk, 'organisation')
    if action == 'post_remove':
        for pk in pk_set:
            organisation = Organisation.objects.get(pk=pk)
            if Document.objects.filter(organisations__in=[organisation]).count() == 0:
                remove_authority_record.delay(pk, 'organisation')


@receiver([m2m_changed], sender=Document.places.through)
def update_place_index(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            add_authority_record.delay(pk, 'place')
    if action == 'post_remove':
        for pk in pk_set:
            place = Place.objects.get(pk=pk)
            if Document.objects.filter(places__in=[place]).count() == 0:
                remove_authority_record.delay(pk, 'place')


@receiver([m2m_changed], sender=Document.events.through)
def update_event_index(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            add_authority_record.delay(pk, 'event')
    if action == 'post_remove':
        for pk in pk_set:
            event = Event.objects.get(pk=pk)
            if Document.objects.filter(events__in=[event]).count() == 0:
                remove_authority_record.delay(pk, 'event')