from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from authority_list.models import Person, Organisation, Event, Place
from authority_list.tasks import index_person, index_event, index_place, index_organisation


@receiver([pre_delete, post_save], sender=Person)
def do_person_index(sender, instance, **kwargs):
    index_person.delay(instance.id)


@receiver([pre_delete, post_save], sender=Organisation)
def do_organisation_index(sender, instance, **kwargs):
    index_organisation.delay(instance.id)


@receiver([pre_delete, post_save], sender=Place)
def do_place_index(sender, instance, **kwargs):
    index_place.delay(instance.id)


@receiver([pre_delete, post_save], sender=Event)
def do_event_index(sender, instance, **kwargs):
    index_event.delay(instance.id)
