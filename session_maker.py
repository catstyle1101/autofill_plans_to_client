import logging
import requests
import os

import const


class SessionMaker:

    session = None

    def __new__(cls, *args, **kwargs):
        if not cls.session:
            cls.session = SessionMaker.create_session()
        return super(SessionMaker, cls).__new__(cls)

    @classmethod
    def create_session(cls):
        logger = logging.getLogger(const.LOGGER_NAME)
        login = os.getenv("USER")
        password = os.getenv("PASSWORD")
        headers = {
            "authority": f"{const.DOMAIN}",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
            ),
            "x-requested-with": "XMLHttpRequest",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "referer": f"https://{const.DOMAIN}/cat/invoice.html",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        }
        auth_data = {"auth[password]": password, "auth[login]": login}
        requests_session = requests.session()
        result = requests_session.get(
            const.LOGIN_URL.format(login, password),
            data=auth_data,
            headers=headers,
        )
        if result.status_code == 200:
            session_id = result.cookies.get("session-id")
            logger.info(f"Connection established. Session ID is {session_id}")
        else:
            err = f'Сервер вернул ошибку {result.status_code} '
            logger.critical(err)
            raise ConnectionError(err)
        return requests_session


class ClientScrapper(SessionMaker):

    def get_client_id(self, client_code):
        url = (
            f"https://{const.DOMAIN}/cat/data-cli.html?login={const.LOGIN}&"
            f"man={const.MAN}&cType1=0&cType2=0&_search=true&nd="
            f"1633502002783&rows=20&page=1&sidx=cli-name"
            f"&sord=asc&cli-code={client_code}&_=1633502002784"
        )
        data = self._get_data_from_url(url)
        return data.get('rows')[0].get('id')

    def get_client_card(self, client_id):
        url = (f"https://{const.DOMAIN}/cat/getrecord.html?man="
               f"{const.MAN}&login={const.LOGIN}&org={client_id}"
               "&mode=getrecord&syf_prog=cli-card")
        data = self._get_data_from_url(url)
        return data

    def get_additional_info(self, client_id: str):
        url = (f"https://{const.DOMAIN}/cat/data-sign.html?file-code=7&"
               f"id={client_id}&_search=false&rows=1000&page=1"
               f"&sidx=name+desc,+&sord=asc&_=1675164424792")
        data = self._get_data_from_url(url)
        return data

    def _get_data_from_url(self, url) -> dict:
        try:
            result = self.session.get(url)
        except Exception as e:
            logging.error(e)
            raise e
        data = result.json()
        if type(data) == list:
            return data
        elif type(data) == list and data[0].get('error'):
            error = data.get('error')
            logging.error(error)
            raise ValueError(error)
        if not data['rows']:
            err = 'Сервер ничего не вернул по клиенту'
            logging.error(err)
            raise ConnectionError(err)
        return data
