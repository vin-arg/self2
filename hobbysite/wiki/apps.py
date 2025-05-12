from django.apps import AppConfig


class WikiConfig(AppConfig):
    """Django App Configuration for the Wiki app."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "wiki"