import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSwaggerInspectorIntegration(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        # Абсолютный путь к файлу спецификации openapi.yaml
        self.openapi_path = os.path.abspath("openapi.yaml")

    def tearDown(self):
        self.driver.quit()

    def test_swagger_inspector_integration(self):
        driver = self.driver
        # Переход на страницу Swagger Inspector
        driver.get("https://inspector.swagger.io")
        # Ждем, пока загрузится базовая структура страницы
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Если на странице используется iframe, переключаемся на него
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            driver.switch_to.frame(iframes[0])

        # Ожидаем появления элемента загрузки файла (input[type='file'])
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )

        # Выполняем загрузку файла спецификации
        file_input.send_keys(self.openapi_path)

        # Ожидаем, пока в теле страницы появится название API, подтверждая успешную загрузку спецификации
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Items API")
        )

        # Если дошли сюда, значит интеграция прошла успешно
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Items API", body_text)


if __name__ == "__main__":
    unittest.main()
