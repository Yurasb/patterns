# Применимость:
# Паттерн Мост особенно полезен когда приходится делать кросс-платформенные приложения,
# поддерживать несколько типов баз данных или работать с разными поставщиками похожего API
# (например, cloud-сервисы, социальные сети и т. д.).
#
# Признаки применения паттерна:
# Если в программе чётко выделены классы «управления» и несколько видов классов «платформ», причём управляющие объекты
# делегируют выполнение платформам, то можно сказать, что используется Мост.


from __future__ import annotations

import string
import random
from abc import ABC, abstractmethod


class AbstractAPI:
    """
    Абстракция устанавливает интерфейс для «управляющей» части двух иерархий классов.
    Она содержит ссылку на объект из иерархии Реализации и делегирует ему всю настоящую работу.
    """

    def __init__(self, api_implementation: "APIImplementation"):
        self.implementation = api_implementation

    def authenticate(self) -> str:
        return self.implementation.login()


class APIImplementation(ABC):
    """
    Реализация устанавливает интерфейс для всех классов реализации. Он не должен соответствовать интерфейсу Абстракции.
    На практике оба интерфейса могут быть совершенно разными.
    Как правило, интерфейс Реализации предоставляет только примитивные операции, в то время как Абстракция определяет
    операции более высокого уровня, основанные на этих примитивах.
    """

    @abstractmethod
    def login(self) -> str:
        pass

    @abstractmethod
    def get_user(self) -> tuple:
        pass


# Каждая Конкретная Реализация соответствует определённой платформе и реализует интерфейс Реализации с использованием
# API этой платформы.


class CloudAPIImplementation(APIImplementation):

    def login(self) -> str:
        user, role = self.get_user()
        return f"Logged to cloud platform as user {user} with role {role}"

    def get_user(self) -> tuple:
        return "CloudUser", self.__class__.__name__


class ExternalAPIImplementation(APIImplementation):

    def login(self) -> str:
        user, role, token = self.get_user()
        return f"Logged to cloud platform via external API token {token} as {user} with role {role}"

    def get_user(self) -> tuple:
        token = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return "ExternalUser", self.__class__.__name__, token


def client_code(api_abstraction: "AbstractAPI") -> None:
    """
    За исключением этапа инициализации, когда объект Абстракции связывается с определённым объектом Реализации,
    клиентский код должен зависеть только от класса Абстракции. Таким образом, клиентский код может поддерживать любую
    комбинацию абстракции и реализации.
    """

    print(api_abstraction.authenticate(), end="")


if __name__ == "__main__":
    # Клиентский код должен работать с любой предварительно сконфигурированной комбинацией абстракции и реализации.

    cloud_api = CloudAPIImplementation()
    abstraction = AbstractAPI(api_implementation=cloud_api)
    client_code(api_abstraction=abstraction)

    print("\n")

    external_api = ExternalAPIImplementation()
    abstraction = AbstractAPI(api_implementation=external_api)
    client_code(api_abstraction=abstraction)
