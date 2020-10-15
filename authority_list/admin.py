from django.contrib import admin
from authority_list.models import OrganisationForm


class OrganisationFormAdmin(admin.ModelAdmin):
    pass


admin.site.register(OrganisationForm, OrganisationFormAdmin)
