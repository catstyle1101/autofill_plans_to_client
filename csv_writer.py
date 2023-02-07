import csv
import os

import const
from logger import set_logger

from models import Client


class CsvFile:

    def __init__(self):
        self.logger = set_logger()
        self.list_of_clients = self.get_list_of_clients()

    def get_list_of_clients(self):
        list_of_clients = list()
        try:
            with open(const.CLIENTS_FILE_NAME, "r",
                      encoding="windows-1251") as f:
                reader = csv.reader(f, dialect="excel", delimiter=",")
                for row in reader:
                    client_code = row[0].split(";")[0]
                    if client_code.isdigit() and (client_code
                                                  not in list_of_clients):
                        list_of_clients.append(client_code)
        except FileNotFoundError as e:
            self.logger.critical(f"Файл {const.CLIENTS_FILE_NAME} не найден")
            raise e
        if list_of_clients == []:
            self.logger.info("Список клиентов пуст")
        return list_of_clients

    def wipe_error_csv(self):
        with open(const.CLIENTS_ERROR_FILE_NAME, "w",
                  encoding='windows-1251', newline='') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(('Код клиента', 'Название клиента', 'Менеджер'))

    def rewrite_clients_csv(self):
        os.remove(const.CLIENTS_FILE_NAME)
        os.rename(const.CLIENTS_ERROR_FILE_NAME, const.CLIENTS_FILE_NAME)
        self.logger.info(
                f"Файл {const.CLIENTS_FILE_NAME} с отчетом сформирован")

    def add_error_client_to_csv(self, client: Client):
        with open(const.CLIENTS_ERROR_FILE_NAME, "a",
                  encoding="windows-1251", newline='') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow((client.code, client.name, client.manager))
