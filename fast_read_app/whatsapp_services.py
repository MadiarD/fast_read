import logging
import os
import time
import traceback
import threading
import queue
import urllib.parse

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
            # Ожидаем, пока исчезнет QR-код (появится поле чата)
            WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            print("Вход в WhatsApp Web выполнен.")
            return driver
        except Exception as e:
            print(f"Ошибка инициализации WebDriver: {e}")
            traceback.print_exc()
            raise

    def _send_message_via_direct_link(self, phone_number, message):
        try:
            # Кодирование сообщения для URL
            encoded_message = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}&app_absent=0"
            
            # Открываем URL для отправки сообщения
            self.driver.get(url)
            
            # Добавляем задержку, чтобы страница успела загрузиться
            time.sleep(5)  # 5 секунд, можно настроить по необходимости
            
            # Определяем XPath кнопки отправки с учётом локализации
            # Для русского интерфейса: aria-label="Отправить"
            # Для английского интерфейса: aria-label="Send"
            send_button_xpath = "//button[@aria-label='Отправить' or @aria-label='Send']"
            send_button = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable((By.XPATH, send_button_xpath))
            )
            
            # Нажимаем кнопку отправки
            send_button.click()
            
            print(f"Сообщение успешно отправлено через прямую ссылку на номер: {phone_number}")
            
            # Ждем, пока сообщение отправится
            time.sleep(5)  # Можно настроить время ожидания по необходимости
            
            # После отправки сообщения через ссылку, возвращаемся на основную страницу
            self.driver.get("https://web.whatsapp.com")
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            # Добавляем небольшую задержку перед следующим сообщением
            time.sleep(2)
            
        except Exception as e:
            print(f"Ошибка при отправке сообщения через прямую ссылку на {phone_number}: {e}")
            traceback.print_exc()

    def _send_message(self, phone_number, message):
        """
        Отправить сообщение через прямую ссылку.
        """
        try:
            self._send_message_via_direct_link(phone_number, message)
        except Exception as e:
            print(f"Не удалось отправить сообщение на номер {phone_number}: {e}")
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
