# Generated by Django 2.2.12 on 2020-05-26 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0006_auto_20200526_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='zotero_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
