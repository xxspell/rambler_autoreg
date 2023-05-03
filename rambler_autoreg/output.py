"""Функция записи данных в файлы"""
from datetime import datetime
import json

# Third-party libraries
from slugify import slugify

# Libraries of this project
from rambler_autoreg.logger import logger
from rambler_autoreg.paths import OUTPUT_DIR


def write(data, filename: str = 'data', *, add_date: bool = True):
    """
    Записывает данные в файл.

    :param data: Данные на запись.
    :param filename: Имя файла. Если обнаружится файл с тем же названием, он будет перезаписан!
    :param add_date: Добавляет дату и время в конец названия файла.
    Если установить значение True, то будет записывать данные в новый файл,
    название которого строится по шаблону "{filename}_{now_datetime}.json".
    """
    logger.info(f'Writing data to a file..')
    if not data:
        logger.warning(f'There is no data to write')
        return

    filename = slugify(filename)
    if add_date:
        now_datetime = f'{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}'
        json_filename = f'{filename}_{now_datetime}.json'
        txt_filename = f'{filename}_{now_datetime}.txt'
    else:
        json_filename = f'{filename}.json'
        txt_filename = f'{filename}.txt'
    json_filepath = OUTPUT_DIR / json_filename
    txt_filepath = OUTPUT_DIR / txt_filename

    with open(json_filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False, default=str)
        # ensure_ascii=False — Для русских символов
        # default=str — Для сериализации datetime.datetime, datetime.date
    logger.success(f'Data was successfully written to the file {json_filepath}')
    with open(txt_filepath, 'w', encoding='utf-8') as file:
        for account in data:
            email = account['email']
            password = account['password']
            secret = account['secret']
            file.write(f'{email}:{password}:{secret}\n')
    logger.success(f'Data was successfully written to the file {json_filepath}')