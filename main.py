from csv_writer import CsvFile
from calculate import ClientParser, PlanWriter
from logger import set_logger


def main():
    list_of_clients = CsvFile().list_of_clients
    all_clients_count = len(list_of_clients)
    logger = set_logger()
    logger.info(f"Всего клиентов: {all_clients_count}. Начинаю работу...")
    for idx, client_code in enumerate(list_of_clients, 1):
        try:
            parser = ClientParser()
            client = parser(client_code)
            PlanWriter(client).post_plans()
        except Exception:
            ...


if __name__ == '__main__':
    main()
