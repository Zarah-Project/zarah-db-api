from django.apps import AppConfig


class DocumentAppConfig(AppConfig):
    name = 'document'

    def ready(self):
        super(DocumentAppConfig, self).ready()
        from document.signals import do_index
