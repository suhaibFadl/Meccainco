from django.apps import AppConfig


class InboxesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inboxes'
    
    def ready(self):
        import inboxes.signals