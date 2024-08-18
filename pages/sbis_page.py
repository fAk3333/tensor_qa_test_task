from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SbisPage(BasePage):
    CONTACTS_LINK = (By.LINK_TEXT, "Контакты")
    TENSOR_BANNER = (By.CSS_SELECTOR, "img[alt='Разработчик системы СБИС — компания «Тензор»']")
    REGION_SELECTOR = (By.CSS_SELECTOR, "span.sbis_ru-Region-Chooser__text.sbis_ru-link")
    CITY_SELECTOR = (By.CSS_SELECTOR, "div#city-id-2.sbisru-Contacts-List__city")
    CRIMEA_BUTTON = (By.XPATH, "//span[text()='Республика Крым']")
    KAMCHATKA_BUTTON = (By.XPATH, "//span[text()='41 Камчатский край']")
    PARTNER_NAME = (By.CSS_SELECTOR, "div.sbisru-Contacts-List__name.sbisru-Contacts-List--ellipsis")
    DOWNLOAD_LINK = (By.XPATH, "//a[text()='Скачать локальные версии']")
    DOWNLOAD_BUTTON = (By.XPATH, "//a[contains(text(), 'Скачать (Exe 11.05 МБ)')]")

    def go_to_contacts(self):
        self.find_element(self.CONTACTS_LINK).click()

    def click_tensor_banner(self):
        # Найти элемент баннера
        element = self.find_element(self.TENSOR_BANNER)

        # Хранение идентификатора основной вкладки
        original_window = self.driver.current_window_handle

        # Клик по элементу
        element.click()

        # Переключение на новую вкладку
        new_window = [window for window in self.driver.window_handles if window != original_window][0]
        self.driver.switch_to.window(new_window)

        # Закрытие старой вкладки
        self.driver.switch_to.window(original_window)
        self.driver.close()

        # Переключение на новую вкладку, так как старая закрыта
        self.driver.switch_to.window(new_window)

    def get_region_text(self):
        try:
            region_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.REGION_SELECTOR)
            )
            return region_element.text
        except TimeoutException:
            print("Не удалось найти элемент с текстом региона")
            return None

    def get_city_text(self):
        try:
            city_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.CITY_SELECTOR)
            )
            return city_element.text
        except TimeoutException:
            print("Не удалось найти элемент с текстом города")
            return None

    def select_region(self):
        # Нажать на кнопку "Республика Крым"
        crimea_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CRIMEA_BUTTON)
        )
        crimea_button.click()

        # Ожидание и нажатие на кнопку "41 Камчатский край" в выпадающем меню
        kamchatka_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.KAMCHATKA_BUTTON)
           )
        kamchatka_button.click()

    def get_partner_name(self):
        try:
            region_name_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.PARTNER_NAME)
            )
            return region_name_element.text
        except TimeoutException:
            print("Не удалось найти элемент с названием региона")
            return None
    def get_page_title(self):
        return self.driver.title

    def go_to_download_page(self):
        # Нажатие на ссылку "Скачать локальные версии"
        self.find_element(self.DOWNLOAD_LINK).click()

    def download_file(self):
        download_button = self.find_element(self.DOWNLOAD_BUTTON)
        download_button.click()