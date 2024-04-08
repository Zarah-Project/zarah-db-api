from django.apps import AppConfig


class DocumentAppConfig(AppConfig):
    name = 'document'

    def ready(self):
        super(DocumentAppConfig, self).ready()
        from document.signals import do_index
        from document.signals import remove_index
        from document.signals import update_person_index
        from document.signals import update_organisation_index
        from document.signals import update_place_index
        from document.signals import update_event_index
