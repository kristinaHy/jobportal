from django.apps import AppConfig


class JobAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_app'

    def ready(self):
        import job_app.signals
