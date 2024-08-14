import os

from django.apps import AppConfig


class PostmailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'postmails'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'True':
            from postmails.services import start_scheduler
            start_scheduler()
