from django.db import models
from model_clone import CloneMixin


class Classification(CloneMixin, models.Model):
    document = models.ForeignKey('document.Document', on_delete=models.CASCADE, related_name='classifications')
    classification_field = models.ForeignKey('ClassificationField', on_delete=models.PROTECT)
    classification_other_text = models.TextField(blank=True)

    _clone_many_to_one_or_one_to_many_fields = ['classification_field']

    class Meta:
        db_table = 'classifications'
        unique_together = ('document', 'classification_field')


class ClassificationCategory(models.Model):
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'classification_categories'
        verbose_name = 'Classification category'
        verbose_name_plural = 'Classification categories'


class ClassificationField(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    category = models.ForeignKey('ClassificationCategory', on_delete=models.PROTECT)
    field_type = models.CharField(max_length=5, choices=[('tag', 'tag'), ('group', 'group'), ('other', 'other')])
    field = models.CharField(max_length=200)

    @property
    def full_name(self):
        if self.parent:
            return "%s -> %s" % (self.parent.full_name, self.field)
        else:
            return self.field

    def __str__(self):
        return "%s -> %s"[0:80] % (self.category.name, self.full_name)

    class Meta:
        db_table = 'classification_fields'


class ClassificationFurtherExplanation(CloneMixin, models.Model):
    document = models.ForeignKey('document.Document', on_delete=models.CASCADE, related_name='explanations')
    category = models.ForeignKey('ClassificationCategory', on_delete=models.PROTECT)
    explanation = models.TextField(blank=True)

    _clone_many_to_one_or_one_to_many_fields = ['category']

    class Meta:
        db_table = 'classification_further_explanations'
        unique_together = ('document', 'category')


class ConsentType(models.Model):
    key = models.CharField(max_length=50)
    group = models.CharField(max_length=50, default='interview')
    type = models.CharField(max_length=400)

    class Meta:
        db_table = 'consent_types'


class DocumentConsent(CloneMixin, models.Model):
    document = models.ForeignKey('document.Document', on_delete=models.CASCADE, related_name='consents')
    consent_type = models.ForeignKey('ConsentType', on_delete=models.CASCADE)
    consent_text = models.TextField(blank=True)
    consent = models.BooleanField(default=False)

    _clone_many_to_one_or_one_to_many_fields = ['consent_type']

    class Meta:
        db_table = 'consents'
        unique_together = ('document', 'consent_type')
