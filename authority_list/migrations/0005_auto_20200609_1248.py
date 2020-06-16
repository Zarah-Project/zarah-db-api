# Generated by Django 2.2.12 on 2020-06-09 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authority_list', '0004_auto_20200526_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationGenderedMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'organisation_gendered_memberships',
            },
        ),
        migrations.AddField(
            model_name='organisation',
            name='organisation_gendered_membership_text',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='organisation',
            name='organisation_gendered_membership',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authority_list.OrganisationGenderedMembership'),
        ),
    ]