# Generated by Django 2.2.12 on 2020-08-06 21:23

from django.db import migrations, models
import django_date_extensions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authority_list', '0005_auto_20200609_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', django_date_extensions.fields.ApproximateDateField()),
                ('date_to', django_date_extensions.fields.ApproximateDateField(blank=True)),
                ('event', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'db_table': 'events',
            },
        ),
    ]
