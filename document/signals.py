from django.db.models.signals import post_save
from django.dispatch import receiver

from document.indexer import DocumentIndexer
from document.models import Document


@receiver([post_save], sender=Document)
def do_index(sender, instance, **kwargs):
    indexer = DocumentIndexer(instance)
    indexer.index()
