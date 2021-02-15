from django.apps import AppConfig


class AuthorityListConfig(AppConfig):
    name = 'authority_list'

    def ready(self):
        super(AuthorityListConfig, self).ready()
        from authority_list.signals import do_person_index
        from authority_list.signals import do_organisation_index
        from authority_list.signals import do_place_index
        from authority_list.signals import do_event_index
