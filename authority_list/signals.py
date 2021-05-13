from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from authority_list.models import Person, Organisation, Event, Place
from authority_list.tasks import index_person, index_event, index_place, index_organisation
from document.models import Document
from document.tasks import index_document_admin, index_document_public


@receiver([pre_delete, post_save], sender=Person)
def do_person_index(sender, instance, **kwargs):
    index_person.delay(instance.id)

    documents = Document.objects.filter(people=instance)
    for document in documents.iterator():
        index_document_admin.delay(document.id)
        index_document_public.delay(document.id)


@receiver([pre_delete, post_save], sender=Organisation)
def do_organisation_index(sender, instance, **kwargs):
    index_organisation.delay(instance.id)

    documents = Document.objects.filter(organisations=instance)
    for document in documents.iterator():
        index_document_admin.delay(document.id)
        index_document_public.delay(document.id)


@receiver([pre_delete, post_save], sender=Place)
def do_place_index(sender, instance, **kwargs):
    index_place.delay(instance.id)

    documents = Document.objects.filter(places=instance)
    for document in documents.iterator():
        index_document_admin.delay(document.id)
        index_document_public.delay(document.id)


@receiver([pre_delete, post_save], sender=Event)
def do_event_index(sender, instance, **kwargs):
    index_event.delay(instance.id)

    documents = Document.objects.filter(events=instance)
    for document in documents.iterator():
        index_document_admin.delay(document.id)
        index_document_public.delay(document.id)