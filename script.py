from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 20)

try:
    driver.get("https://my.telegram.org/auth")

    print("HTML страницы:")
    print(driver.page_source[:1000])

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        print(f"Найдено {len(iframes)} iframe, переключаемся на первый.")
        driver.switch_to.frame(iframes[0])
    else:
        print("iframe не найдены, продолжаем работу с основной страницей.")

    phone_input = wait.until(EC.presence_of_element_located((By.NAME, "phone")))

    wait.until(EC.visibility_of(phone_input))

    driver.execute_script("arguments[0].scrollIntoView(true);", phone_input)

    wait.until(EC.element_to_be_clickable((By.NAME, "phone")))

    phone_number = "+1234567890"
    phone_input.send_keys(phone_number)

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    submit_button.click()

    time.sleep(3)

    print("Сценарий выполнен: номер телефона отправлен.")

except Exception as e:
    print("Произошла ошибка:", e)

finally:
    driver.quit()
