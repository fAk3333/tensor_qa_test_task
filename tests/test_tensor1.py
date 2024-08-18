import time
from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Обработчик для вывода логов в файл
file_handler = logging.FileHandler('test_log1.log', mode='w')
file_handler.setLevel(logging.INFO)

# Обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def test_tensor_page(driver):
    logger.info("Переход на сайт sbis.ru")
    sbis_page = SbisPage(driver)
    sbis_page.go_to_site("https://sbis.ru")

    logger.info("Переход в раздел 'Контакты'")
    sbis_page.go_to_contacts()

    logger.info("Клик по баннеру Тензор")
    sbis_page.click_tensor_banner()

    logger.info("Переход на сайт tensor.ru")
    tensor_page = TensorPage(driver)

    logger.info("Проверка наличия блока 'Сила в людях'")
    assert tensor_page.check_people_power_section(), "Блок 'Сила в людях' не найден"

    logger.info("Переход в 'Подробнее' и проверка перехода на страницу 'about'")
    tensor_page.click_more_details()

    logger.info("Проверка URL на соответствие https://tensor.ru/about")
    assert driver.current_url == "https://tensor.ru/about", "Не удалось перейти на страницу 'about'"

    logger.info("Проверка размеров изображений в разделе 'Работаем'")
    dimensions = tensor_page.get_work_images_dimensions()
    assert len(dimensions) > 0, "Не найдены изображения в разделе 'Работаем'"
    first_dimension = dimensions[0]
    assert first_dimension != (None, None), "Картинки не приняты"
    logger.info(f'размер картинки #1 {first_dimension}')

    for i, dimension in enumerate(dimensions, start=1):
        if dimension != (None, None):  # Проверка только для найденных изображений
            logger.info(f'размер картинки #{i} - {dimension}')
            assert dimension == first_dimension, "Размеры изображений в хронологии различаются"

    logger.info("Тест успешно завершен.")

