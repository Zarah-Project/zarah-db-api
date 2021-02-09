from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from document.indexers.indexer import DocumentIndexer
from document.models import Document


@receiver([post_save], sender=Document)
def do_index(sender, instance, **kwargs):
    indexer = DocumentIndexer(instance)
    indexer.index()


@receiver([pre_delete], sender=Document)
def remove_index(sender, instance, **kwargs):
    indexer = DocumentIndexer(instance)
    indexer.remove_record()
