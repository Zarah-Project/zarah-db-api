# Generated by Django 2.2.12 on 2020-08-12 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority_list', '0006_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['date_from', 'date_to', 'event']},
        ),
        migrations.AddField(
            model_name='place',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
