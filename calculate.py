import requests

import const
from models import Client, Potential, Plan
from session_maker import ClientScrapper
from logger import set_logger


class ClientParser:
    def __init__(self):
        self.client = None
        self.logger = set_logger() # тут и везде. это жесткая зависисоть от модуля. Лучше испольтзовать иньекцию зависимостей через параметр конструктора. Так парсеру можно будет скормить любой логгер, который обладает нужным интерфейсом

    def __call__(self, client_code: str) -> Client:
        self.client = self.parse_client(client_code)  # вроде нигде не используется больше в классе. Нужно ли его паковать в объект? Или где-то наружу нужно отдавать клиента?
        return self.client

    def parse_data(
        self,
        code_client: str,
        client_id: str,
        client_data: list[dict],
        client_additional_data: dict,
    ) -> Client:
        try:
            row = client_data[0]
        except IndexError:
            message = (
                "Ошибка индекса ответа базы при поиске клиента, "
                "в функции: parse_data"
            )
            self.logger.error(message)
            raise IndexError(message)
        plan = None
        for i in client_additional_data.get("rows"):  # что такое i? 
            if i.get("code") == "478":  # 478 стоит сунуть в константу. Как и все остальные жестко заданные данные
                year = int(i.get("val").split()[1][-4:])  # сложная конструкция для восприятия
                if year != const.PLAN_YEAR:
                    continue
                plan = Plan(id=i.get("id"), year=year)
        client = Client(
            client_id=client_id,
            code=code_client,
            name=row.get("name"),
            potential_electric=getattr(
                Potential, row.get("cli_172_potent"), Potential.dR
            ),
            potential_krep=getattr(
                Potential, row.get("cli_173_potent"), Potential.bR
            ),
            potential_sb=getattr(
                Potential, row.get("cli_174_potent"), Potential.aR
            ),
            spk_electric=int(row.get("cli_172_potent_d")),
            spk_krep=int(row.get("cli_173_potent_d")),
            spk_sb=int(row.get("cli_174_potent_d")),
            plan_id=plan,
        )
        self.validate_client_spk(client)
        return client

    def parse_client(self, code_client: str) -> Client:
        client = ClientScrapper()
        client_id = client.get_client_id(code_client)
        client_additional_data = client.get_additional_info(client_id)
        client_data = client.get_client_card(code_client)
        client = ClientParser.parse_data( # тут точно нужен статический вызов? не self.parse_data(...)?
            self,
            code_client=code_client,
            client_id=client_id,
            client_data=client_data,
            client_additional_data=client_additional_data,
        )
        if self.validate_client_spk(client):
            return client

    def validate_client_spk(self, client: Client) -> bool:
        for potential, spk in (
            (client.potential_electric, client.spk_electric),
            (client.potential_krep, client.spk_krep),
            (client.potential_sb, client.spk_sb),
        ):
            if spk != 0 and (
                potential.value.min is None or potential.value.max is None
            ):
                message = (
                    f"Клиент {client.code} {client.name}: Потенциал "
                    f"{potential.name}, надо изменить"
                )
                self.logger.error(message)
                raise ValueError(message)
            elif not potential.value.min <= spk <= potential.value.max:
                message = (
                    f"Клиент {client.code} {client.name}: "
                    f"Потенциал {potential.name} не "
                    f"соответствует СПК {spk} "
                    f"рамки: от {potential.value.min} до "
                    f"{potential.value.max}"
                )
                self.logger.error(message)
                raise ValueError(message)
        return True


class PlanWriter:

    logger = set_logger()

    def __init__(self, client: Client):
        self.client = client
        self.plan_to_write = dict()
        self.calculate_plan()

    def calculate_plan(self):
        self.plan_to_write["overall_potential"] = (
            self.client.spk_electric
            + self.client.spk_krep
            + self.client.spk_sb
        ) * 1000  # тут и ниже. Эта 1000 означает одно и то же? Если да, то стопроцентная константа

        self.plan_to_write["plan_ours"] = (
            int(
                self.plan_to_write.get("overall_potential")
                * const.SHARE_CLIENT_PLAN
            )
            * 1000
        )

        self.plan_to_write["electric_potentials"] = [
            int(i * self.client.spk_electric * const.SHARE_CLIENT_PLAN) * 1000
            for i in const.RAISE_PLAN_BY_Q
        ]

        self.plan_to_write["write_overall_plan"] = [
            str(self.plan_to_write.get("overall_potential") * i)
            for i in const.RAISE_PLAN_BY_Q
        ]

        for key, share in const.SHARES_ELECTIRIC_DIVISION.items(): # я бы переписал в виде спискового выражения, как выше
            plan = list()
            for idx in range(len(const.RAISE_PLAN_BY_Q)):
                plan.append(
                    str(
                        self.plan_to_write.get("electric_potentials")[idx]
                        * share
                    )
                )
            self.plan_to_write[f"write_{key}"] = plan

        self.plan_to_write["write_our_plan"] = [
            str(mul * self.plan_to_write.get("plan_ours"))
            for mul in const.RAISE_PLAN_BY_Q
        ]

        self.plan_to_write["write_sb"] = [
            str(i * self.client.spk_sb * const.SHARE_CLIENT_PLAN * 1000)
            for i in const.RAISE_PLAN_BY_Q
        ]

        self.plan_to_write["write_krep"] = [
            str(i * self.client.spk_krep * const.SHARE_CLIENT_PLAN * 1000)
            for i in const.RAISE_PLAN_BY_Q
        ]

    def post_plans(self):
        url = (  # по хорошему, это тоже должно стать константой и заполнятся тут через format
            f"https://{const.DOMAIN}/cat/data-sign-478s.html?"
            f"org={self.client.code}&login={const.LOGIN}&man={const.MAN}"
            f"&regionPl=%D0%A3&yearPl={const.PLAN_YEAR}"
            f"&pot_fact="
            f'{";".join(self.plan_to_write.get("write_overall_plan"))}'
            f'&pot_cond='
            f'{";".join(self.plan_to_write.get("write_our_plan"))}'
            f'&clsAdmit_1=11;'
            f'{";".join(self.plan_to_write.get("write_kpp"))};'
            f'&clsAdmit_2=13;'
            f'{";".join(self.plan_to_write.get("write_peo"))};'
            f'&clsAdmit_3=14;'
            f'{";".join(self.plan_to_write.get("write_st"))};'
            f'&clsAdmit_4=16;'
            f'{";".join(self.plan_to_write.get("write_ueo"))};'
            f"&clsAdmit_5=1%D0%91;"
            f'{";".join(self.plan_to_write.get("write_sb"))};'
            f"&clsAdmit_6=1F;0;0;0;0;&clsAdmit_7=1S;"
            f'{";".join(self.plan_to_write.get("write_krep"))};'
            f"&clsAdmitCnt=7&oper="
        )
        if self.client.plan_id:
            add = f"edit&id={self.client.plan_id.id}"
        else:
            add = "add"
        url += add
        result = requests.get(url)
        if result.text == 'success':
            message = (f"Клиент: {self.client.code}, {self.client.name} "
                       f"- план на {self.client.plan_id.year} год записан")
            self.logger.info(message)
        else:
            self.logger.error(f"План клиенту {self.client.code}, "
                              f"{self.client.name} "
                              "Не записан")
