from calculate import ClientParser, PlanWriter
from csv_writer import CsvFile
from logger import set_logger
from models import CountClients


def main():
    csv_file = CsvFile()
    list_of_clients = csv_file.list_of_clients
    all_clients_count = len(list_of_clients)
    logger = set_logger()
    logger.info(f"Всего клиентов: {all_clients_count}. Начинаю работу...")
    csv_file.wipe_error_csv()
    for client_code in list_of_clients:
        try:
            parser = ClientParser()
            client = parser(client_code)
            if client:
                PlanWriter(client).post_plans()
        except ValueError:
            ...
        except Exception as e:
            logger.error(e)
    csv_file.rewrite_clients_csv()


if __name__ == '__main__':
    main()
