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
        
        # Указываем user-data-dir для сохранения сессии
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
            driver.maximize_window()
            driver.get("https://web.whatsapp.com")
            
            # Ожидаем, пока пользователь войдет в систему
            print("Пожалуйста, войдите в WhatsApp Web, если еще не вошли.")
            WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
            )
            print("Вход в WhatsApp Web выполнен.")
            return driver
        except Exception as e:
            print(f"Ошибка инициализации WebDriver: {e}")
            traceback.print_exc()
            raise

    def _send_message(self, phone_number, message):
        try:
            # Используем функцию поиска для нахождения контакта по номеру телефона
            search_box_xpath = "//div[@contenteditable='true'][@data-tab='3']"
            search_box = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, search_box_xpath))
            )
            search_box.clear()
            search_box.send_keys(phone_number)
            search_box.send_keys(Keys.ENTER)
            
            # Ждем, пока загрузится поле ввода сообщения
            input_box_xpath = "//footer//div[@contenteditable='true'][@data-tab='10']"
            input_box = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_box_xpath))
            )
            input_box.send_keys(message)
            input_box.send_keys(Keys.ENTER)

            print(f"Сообщение успешно отправлено на номер: {phone_number}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения на {phone_number}: {e}")
            traceback.print_exc()

    def _worker(self):
        try:
            self.driver = self._initialize_driver()

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
