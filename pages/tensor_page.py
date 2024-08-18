from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TensorPage(BasePage):
    # Попробуем более простой локатор для блока "Сила в людях"
    PEOPLE_POWER_SECTION = (By.CSS_SELECTOR,
                            "#container > div.tensor_ru-content_wrapper > div > div.tensor_ru-Index__block4-bg > div > div > div:nth-child(1) > div > p.tensor_ru-Index__card-title.tensor_ru-pb-16")

    # Обновим локатор для ссылки "Подробнее" на более общий
    MORE_DETAILS_LINK = (By.XPATH,
                         "/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/div[5]/div/div/div[1]/div/p[4]/a")

    WORK_SECTION_SELECTORS = [
        "//img[@alt='Разрабатываем систему СБИС']",
        "//img[@alt='Продвигаем сервисы']",
        "//img[@alt='Создаем инфраструктуру']",
        "//img[@alt='Сопровождаем клиентов']"
    ]

    def check_people_power_section(self):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.PEOPLE_POWER_SECTION)
            )
            return element
        except TimeoutException:
            print("Блок 'Сила в людях' не найден")
            return None

    def click_more_details(self):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.MORE_DETAILS_LINK)
        )
        self.driver.execute_script("arguments[0].click();", element)

    def click_more_details(self):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.MORE_DETAILS_LINK)
        )
        self.driver.execute_script("arguments[0].click();", element)

    def get_work_images_dimensions(self):
        dimensions = []
        for xpath in self.WORK_SECTION_SELECTORS:
            try:
                element = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                width = element.get_attribute('width')
                height = element.get_attribute('height')
                dimensions.append((int(width), int(height)))
            except TimeoutException:
                print(f"Изображение с XPath {xpath} не найдено")
                dimensions.append((None, None))  # Добавляем пустое значение, если элемент не найден

        # Вывод размеров для отладки
        for i, (width, height) in enumerate(dimensions):
            if width is not None and height is not None:
                print(f"Изображение {i + 1}: ширина={width}, высота={height}")
            else:
                print(f"Изображение {i + 1} не найдено")

        return dimensions