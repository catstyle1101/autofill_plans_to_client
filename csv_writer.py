import csv

import const
from logger import set_logger


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
                    if client_code.isdigit():
                        list_of_clients.append(client_code)
        except FileNotFoundError as e:
            self.logger.critical(f"Файл {const.CLIENTS_FILE_NAME} не найден")
            raise e
        if list_of_clients == []:
            self.logger.info("Список клиентов пуст")
        return list_of_clients
