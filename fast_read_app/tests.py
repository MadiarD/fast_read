from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import traceback
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.DEBUG)

def send_whatsapp_message(phone_number, message):
    chrome_driver_path = r"C:\chromedriver-win64\chromedriver.exe"

    if not os.path.isfile(chrome_driver_path):
        raise FileNotFoundError(f"ChromeDriver не найден по указанному пути: {chrome_driver_path}")

    service = Service(executable_path=chrome_driver_path)
    options = Options()
    user_profile = r"C:\Users\Madiyar\AppData\Local\Google\Chrome\User Data\Default"
    options.add_argument(f"--user-data-dir={user_profile}")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Ошибка инициализации драйвера: {e}")
        traceback.print_exc()
        return

    try:
        driver.get("https://web.whatsapp.com/")

        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Новый чат']"))
            )
            print("Успешно вошли в WhatsApp Web.")
        except Exception:
            print("Пожалуйста, отсканируйте QR-код для входа в WhatsApp Web.")
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!']"))
            )
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Новый чат']"))
            )
            print("Успешно вошли в WhatsApp Web.")

        url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        driver.get(url)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//footer//div[@contenteditable='true']"))
        )

        input_box = driver.find_element(By.XPATH, "//footer//div[@contenteditable='true']")
        input_box.send_keys(Keys.ENTER)

        print(f"Сообщение успешно отправлено на номер: {phone_number}")
    except Exception as e:
        print("Произошла ошибка:")
        traceback.print_exc()
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    phone_number = "+77781076714"
    message = "whatsapp selenium работает урааа!!!" 
    send_whatsapp_message(phone_number, message)
