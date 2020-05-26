from django.contrib import admin

from metadata.models import ClassificationField, ClassificationCategory


class ClassificationFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'parent', 'field', 'field_type')
    list_editable = ('category', 'parent', 'field', 'field_type')
    list_filter = ('category', )


class ClassificationCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(ClassificationField, ClassificationFieldAdmin)
admin.site.register(ClassificationCategory, ClassificationCategoryAdmin)
