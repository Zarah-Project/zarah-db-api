# Generated by Django 2.2.12 on 2021-06-07 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0009_auto_20210512_2004'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classificationfield',
            options={'ordering': ['ordering', 'id']},
        ),
    ]