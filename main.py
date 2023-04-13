from arg_parser import parse_argv
from calculate import ClientParser, PlanWriter
from csv_writer import CsvFile
from logger import set_logger


def write_plan(client_code):
    try:
        parser = ClientParser()
        client = parser(client_code)
        if client:
            PlanWriter(client).post_plans()
    except ValueError:
        ...
    except Exception as e:
        set_logger().error(e)
        raise e


def main():
    argv = parse_argv()
    csv_file = CsvFile()
    if not argv:
        list_of_clients = csv_file.list_of_clients
    else:
        csv_file.list_of_clients = argv
        list_of_clients = argv

    logger = set_logger()
    logger.info(f"Всего клиентов: {len(list_of_clients)}. Начинаю работу...")

    for client_code in list_of_clients:
        write_plan(client_code)
    csv_file.rewrite_clients_csv()


if __name__ == '__main__':
    main()
