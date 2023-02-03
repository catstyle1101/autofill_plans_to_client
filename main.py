from calculate import ClientParser, PlanWriter
from csv_writer import CsvFile
from logger import set_logger


def main():
    csv_file = CsvFile()
    list_of_clients = csv_file.list_of_clients
    error_clients = list()
    all_clients_count = len(list_of_clients)
    logger = set_logger()
    logger.info(f"Всего клиентов: {all_clients_count}. Начинаю работу...")
    for client_code in list_of_clients:
        try:
            parser = ClientParser()
            client = parser(client_code)
            PlanWriter(client).post_plans()
        except ValueError:
            error_clients.append(client_code)
        except Exception:
            ...
    csv_file.rewrite_clients_csv(error_clients)


if __name__ == '__main__':
    main()
