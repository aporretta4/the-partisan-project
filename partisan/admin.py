from django.contrib import admin
from partisan.models import pull_configuration, sentiment_process_configuration

# Register your models here.
admin.site.register(pull_configuration)
admin.site.register(sentiment_process_configuration)