# Generated by Django 2.2.12 on 2021-06-07 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority_list', '0010_auto_20210510_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='organisation',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='person',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='place',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]