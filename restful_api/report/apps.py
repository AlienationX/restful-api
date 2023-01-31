from django.apps import AppConfig

print("executing ... report.apps.py")

class ReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'report'
