import time
from pages.sbis_page import SbisPage
import logging

# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Обработчик для вывода логов в файл
file_handler = logging.FileHandler('test_log2.log', mode='w')
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

    # Проверка региона
    region_text = sbis_page.get_region_text()
    logger.info(f"Регион определен: {region_text}")
    assert region_text == "Республика Крым", f"Ожидался регион 'Республика Крым', но найден '{region_text}'"

    # Проверка списка партнеров
    city_text = sbis_page.get_city_text()
    logger.info(f"Город: {city_text}")
    assert city_text == "Симферополь", f"Ожидался список партнеров 'Симферополь', но найден '{city_text}'"

    logger.info("Выбор региона '41 Камчатский край'")
    sbis_page.select_region()

    # Повторная проверка региона после выбора
    time.sleep(1)
    region_text_after_selection = sbis_page.get_region_text()
    logger.info(f"Регион после выбора: {region_text_after_selection}")
    assert region_text_after_selection == "Камчатский край", f"Ожидался регион '41 Камчатский край', но найден '{region_text_after_selection}'"

    region_text = sbis_page.get_region_text()
    logger.info(f"Регион определен: {region_text}")
    assert region_text == "Камчатский край", f"Ожидался регион 'Камчатский край', но найден '{region_text}'"

    city_text = sbis_page.get_city_text()
    logger.info(f"Список город: {city_text}")
    assert city_text == "Петропавловск-Камчатский", f"Ожидался список партнеров 'Петропавловск-Камчатский', но найден '{city_text}'"

    logger.info(f'Проверка что 41-kamchatskij-kraj есть в ссылке {driver.current_url}')
    assert '41-kamchatskij-kraj' in driver.current_url, '41-kamchatskij-kraj нет в ссылке'

    partner_name_text = sbis_page.get_partner_name()
    logger.info(f"Название партнёра после выбора: {partner_name_text}")
    assert partner_name_text == "СБИС - Камчатка", f"Ожидалось название региона 'СБИС - Камчатка', но найден '{partner_name_text}'"

    page_title = sbis_page.get_page_title()
    logger.info(f"Тайтл страницы: {page_title}")
    assert "Камчатский край" in page_title, f"Ожидался тайтл, содержащий 'Камчатский край', но найден '{page_title}'"

    logger.info("Тест успешно завершен.")