from django.contrib import admin

from metadata.models import ClassificationField, ClassificationCategory, ConsentType


class ClassificationFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'ordering', 'category', 'parent', 'field', 'field_type')
    list_editable = ('field', 'ordering')
    list_filter = ('category', )


class ClassificationCategoryAdmin(admin.ModelAdmin):
    pass


class ConsentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'type', 'key')


admin.site.register(ClassificationField, ClassificationFieldAdmin)
admin.site.register(ClassificationCategory, ClassificationCategoryAdmin)
admin.site.register(ConsentType, ConsentTypeAdmin)
