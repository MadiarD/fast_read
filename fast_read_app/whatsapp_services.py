import logging
import os
import time
import traceback
import threading
import queue

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка логирования Selenium
LOGGER.setLevel(logging.INFO)

class WhatsAppSender:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(WhatsAppSender, cls).__new__(cls)
        return cls._instance

    def __init__(self, chrome_driver_path, user_profile, chrome_binary, wait_time=30):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.chrome_driver_path = chrome_driver_path
        self.user_profile = user_profile
        self.chrome_binary = chrome_binary
        self.wait_time = wait_time
        self.message_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.driver = None
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()
        self._initialized = True

    def _initialize_driver(self):
        if not os.path.isfile(self.chrome_driver_path):
            raise FileNotFoundError(f"ChromeDriver не найден по пути: {self.chrome_driver_path}")

        service = Service(executable_path=self.chrome_driver_path)
        options = Options()
        
        # Не указывайте user-data-dir, чтобы использовать временный профиль
        options.add_argument(f"--user-data-dir={self.user_profile}")
        
        options.binary_location = self.chrome_binary
        
        # Дополнительные опции для стабильности
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        # Если необходимо, добавьте headless режим
        # options.add_argument("--headless")

        try:
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e:
            print(f"Ошибка инициализации WebDriver: {e}")
            traceback.print_exc()
            raise


    def _send_message(self, phone_number, message):
        try:
            url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
            self.driver.get(url)

            # Ожидаем загрузки поля ввода сообщения
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//footer//div[@contenteditable='true']"))
            )

            input_box = self.driver.find_element(By.XPATH, "//footer//div[@contenteditable='true']")
            input_box.send_keys(Keys.ENTER)

            print(f"Сообщение успешно отправлено на номер: {phone_number}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения на {phone_number}: {e}")
            traceback.print_exc()

    def _worker(self):
        try:
            self.driver = self._initialize_driver()

            # Предполагаем, что пользователь уже вошёл в WhatsApp Web
            print("WebDriver инициализирован. Предполагается, что пользователь уже вошёл в WhatsApp Web.")

            while not self.stop_event.is_set():
                try:
                    phone_number, message = self.message_queue.get(timeout=1)
                    self._send_message(phone_number, message)
                    self.message_queue.task_done()
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Неожиданная ошибка в фоновом потоке: {e}")
                    traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()

    def send_whatsapp_message(self, phone_number, message):
        """Добавить сообщение в очередь для отправки."""
        self.message_queue.put((phone_number, message))

    def shutdown(self):
        """Остановить фоновый поток и закрыть WebDriver."""
        self.stop_event.set()
        if self.thread.is_alive():
            try:
                self.thread.join(timeout=10)  # Устанавливаем таймаут, чтобы избежать зависания
                print("Фоновый поток успешно завершён.")
            except Exception as e:
                print(f"Ошибка при завершении фонового потока: {e}")
                traceback.print_exc()
        else:
            print("Фоновый поток уже завершён.")
