# Generated by Django 2.2.12 on 2020-10-10 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority_list', '0007_auto_20200812_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='internal_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organisation',
            name='internal_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='internal_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='internal_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
