import time
from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os

# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Обработчик для вывода логов в файл
file_handler = logging.FileHandler('test_log3.log', mode='w')
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

def get_latest_file(download_directory):
    """
    Получить путь к последнему загруженному файлу в указанной директории.
    """
    files = [os.path.join(download_directory, f) for f in os.listdir(download_directory)]
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)  # Получаем самый последний файл по времени создания
    return latest_file

def test_tensor_page(driver):

    download_directory = "C://Users/xD/Downloads/"

    logger.info("Переход на сайт sbis.ru")
    sbis_page = SbisPage(driver)
    sbis_page.go_to_site("https://sbis.ru")

    logger.info("Переход на страницу 'Скачать локальные версии'")
    sbis_page.go_to_download_page()

    WebDriverWait(driver, 10).until(EC.url_contains("/download"))
    assert "/download" in driver.current_url, "Не удалось перейти на страницу 'Скачать локальные версии'"

    logger.info("Нажатие на кнопку 'Скачать (Exe 11.05 МБ)'")
    sbis_page.download_file()

    # Даем время для скачивания файла
    logger.info("Ожидание завершения скачивания файла...")
    time.sleep(6)  # Подберите время в зависимости от размера файла и скорости интернета

    # Получаем последний загруженный файл
    latest_file = get_latest_file(download_directory)

    if latest_file:
        file_name = os.path.basename(latest_file)
        file_size = os.path.getsize(latest_file)

        logger.info(f"Имя файла: {file_name}")
        logger.info(f"Размер файла: {file_size / (1024 * 1024):.2f} МБ")  # Размер в мегабайтах
    else:
        logger.error("Не удалось найти загруженный файл.")

    logger.info('Проверка размера файла')
    assert f"{file_size / (1024 * 1024):.2f}" in 'Скачать (Exe 11.05 МБ)'

    logger.info('Тест кейс успешно выполнен')