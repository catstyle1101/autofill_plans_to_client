import os

from dotenv import load_dotenv

load_dotenv()

INDEX_SUM = 14
DOMAIN = os.getenv('DOMAIN')
LOGIN_URL = os.getenv('LOGIN_URL')
LOGIN = os.getenv('USER')
MAN = os.getenv('MAN')
LOGGER_NAME = 'logger'
CLIENTS_FILE_NAME = 'clients.csv'
CONSOLE_LOGGER_NAME = 'console_logger'
PLAN_YEAR = 2023
SHARE_CLIENT_PLAN = 0.33
SHARES_ELECTIRIC_DIVISION = {'kpp': 0.3, 'peo': 0.1, 'st': 0.25, 'ueo': 0.35}
RAISE_PLAN_BY_Q = (1.0, 1.03, 1.06, 1.09)
YEAR = 2023
