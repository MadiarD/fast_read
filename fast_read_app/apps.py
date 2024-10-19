from django.apps import AppConfig
import os
import sys
import atexit
from django.conf import settings

class FastReadAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fast_read_app'
    # def ready(self):
    #     from fast_read_app.whatsapp_services import WhatsAppSender
    #     chrome_driver_path = settings.CHROME_DRIVER_PATH
    #     user_profile = settings.USER_PROFILE
    #     chrome_binary = settings.CHROME_BINARY

    #     # Создаём экземпляр отправителя
    #     sender = WhatsAppSender(
    #         chrome_driver_path=chrome_driver_path,
    #         user_profile=user_profile,
    #         chrome_binary=chrome_binary,
    #         wait_time=60,
    #     )
    #     sender.send_whatsapp_message("+77083137442", "Привет от Selenium!")
    #     # Сохраняем экземпляр в атрибуте модуля для доступа из других мест
    #     current_module = sys.modules[__name__]
    #     current_module.sender = sender

    #     # Регистрируем функцию shutdown для вызова при завершении процесса
    #     atexit.register(sender.shutdown)
