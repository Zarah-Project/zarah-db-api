import uuid as uuid

from django.conf import settings
from django.db import models


class Document(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    record_type = models.CharField(max_length=20, default='default')
    attachment_type = models.CharField(max_length=20, default='default')
    citation_link = models.TextField(blank=True)
    title = models.CharField(max_length=400)
    item_type = models.CharField(max_length=50, blank=True)
    abstract = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    additional_research = models.TextField(blank=True)
    related_documents = models.ManyToManyField('self', blank=True)
    people = models.ManyToManyField('authority_list.Person', blank=True)
    organisations = models.ManyToManyField('authority_list.Organisation', blank=True)
    places = models.ManyToManyField('authority_list.Place', blank=True)
    events = models.ManyToManyField('authority_list.Event', blank=True)

    zotero_id = models.CharField(max_length=100, blank=True)
    zotero_data = models.TextField(blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'documents'


class DocumentFile(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='files')
    sequence = models.IntegerField(blank=True, null=True)
    file_id = models.CharField(max_length=30, default='')
    file_url = models.CharField(max_length=200, default='')
    file = models.FileField(blank=True, null=True)

    class Meta:
        db_table = 'document_files'


class DocumentTriggeringFactorKeyword(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='triggering_factor_keywords')
    keyword = models.CharField(max_length=100)

    class Meta:
        db_table = 'document_triggering_factor_keywords'


class DocumentKeyword(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='keywords')
    keyword = models.CharField(max_length=100)

    class Meta:
        db_table = 'document_keywords'
