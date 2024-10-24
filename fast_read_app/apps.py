from django.apps import AppConfig
import os
import sys
import atexit
from django.conf import settings

class FastReadAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fast_read_app'
   