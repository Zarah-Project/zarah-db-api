from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from authority_list.models import Person, Organisation, Event, Place
from authority_list.tasks import index_document_person, index_document_organisation, index_document_place, \
    index_document_event, remove_authority_record, add_authority_record
from document.models import Document


@receiver([pre_delete, post_save], sender=Person)
def do_person_index(sender, instance, action, **kwargs):
    index_document_person.delay(instance.id)

    if action == 'pre_delete':
        remove_authority_record.delay(instance.id, 'person')
    else:
        if Document.objects.filter(people__in=[instance]).count() > 0:
            add_authority_record.delay(instance.id, 'person')


@receiver([pre_delete, post_save], sender=Organisation)
def do_organisation_index(sender, instance, action, **kwargs):
    index_document_organisation.delay(instance.id)

    if action == 'pre_delete':
        remove_authority_record.delay(instance.id, 'organisation')
    else:
        if Document.objects.filter(organisations__in=[instance]).count() > 0:
            add_authority_record.delay(instance.id, 'organisation')


@receiver([pre_delete, post_save], sender=Place)
def do_place_index(sender, instance, action, **kwargs):
    index_document_place.delay(instance.id)

    if action == 'pre_delete':
        remove_authority_record.delay(instance.id, 'place')
    else:
        if Document.objects.filter(places__in=[instance]).count() > 0:
            add_authority_record.delay(instance.id, 'place')


@receiver([pre_delete, post_save], sender=Event)
def do_event_index(sender, instance, action, **kwargs):
    index_document_event.delay(instance.id)

    if action == 'pre_delete':
        remove_authority_record.delay(instance.id, 'event')
    else:
        if Document.objects.filter(events__in=[instance]).count() > 0:
            add_authority_record.delay(instance.id, 'event')
