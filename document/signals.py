from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

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
