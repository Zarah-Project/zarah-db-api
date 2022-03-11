from django.contrib import admin
from document.models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'item_type')
    list_editable = ('title', 'item_type')
    list_filter = ('item_type', )


admin.site.register(Document, DocumentAdmin)
