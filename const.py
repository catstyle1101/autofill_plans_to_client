import os

from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv('DOMAIN')
LOGIN_URL = os.getenv('LOGIN_URL')
LOGIN = os.getenv('USER')
MAN = os.getenv('MAN')
LOGGER_NAME = 'logger'
CLIENTS_FILE_NAME = 'clients.csv'
CLIENTS_ERROR_FILE_NAME = 'errors.csv'
CONSOLE_LOGGER_NAME = 'console_logger'
PLAN_CODE = "478"
PLAN_YEAR = 2023
SHARE_CLIENT_PLAN = 0.6
SHARES_ELECTIRIC_DIVISION = {'kpp': 0.3, 'peo': 0.1, 'st': 0.25, 'ueo': 0.35}
RAISE_PLAN_BY_Q = (1.0, 1.03, 1.06, 1.09)
THOUSANDS = 1000
WRITE_PLAN_URL = (
    f"https://{DOMAIN}/cat/data-sign-478s.html?org="
    "{client_code}"
    f'&login={LOGIN}&man={MAN}&regionPl=%D0%A3&yearPl={PLAN_YEAR}'
    '&pot_fact={plan}&pot_cond={our_plan}'
    '&clsAdmit_1=11;{kpp};&clsAdmit_2=13;{peo};'
    '&clsAdmit_3=14;{st};&clsAdmit_4=16;{ueo};'
    '&clsAdmit_5=1%D0%91;{sb};&clsAdmit_6=1F;0;0;0;0;'
    '&clsAdmit_7=1S;{krep};&clsAdmitCnt=7&oper='
)
CLIENT_ID_URL = (
        f"https://{DOMAIN}/cat/data-cli.html?login={LOGIN}&"
        f"man={MAN}&cType1=0&cType2=0&_search=true&nd="
        "1633502002783&rows=20&page=1&sidx=cli-name"
        "&sord=asc&cli-code={client_code}&_=1633502002784"
)
CLIENT_CARD_URL = (
    f"https://{DOMAIN}/cat/getrecord.html?man="
    f"{MAN}&login={LOGIN}&org="
    "{client_code}&mode=getrecord&syf_prog=cli-card"
)
CLIENT_ADD_CARD_URL = (
    f"https://{DOMAIN}/cat/data-sign.html?file-code=7&"
    "id={client_id}&_search=false&rows=1000&page=1"
    "&sidx=name+desc,+&sord=asc&_=1675164424792"
)
SPK_ERROR_MESSAGE = (
    "Менеджер: {manager} "
    "Клиент {client_code} {client_name}: "
    "Потенциал {potential_name} не "
    "соответствует СПК {spk} "
    "рамки: от {potential_value_min} до "
    "{potential_value_max}"
)
SUCCESS_WRITE_MESSAGE = (
    "({count}) "
    "Клиент: {client_code}, {client_name} "
    "- план на {client_plan_id_year} год записан"
)
ERROR_WRITE_MESSAGE = (
    "({count}) "
    "План клиенту {client_code}, "
    "{client_name} "
    "Не записан"
)
