# Generated by Django 2.2.12 on 2020-05-26 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0005_documenttriggeringfactorkeyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='file_id',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='sequence',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
