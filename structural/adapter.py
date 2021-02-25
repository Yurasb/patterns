# Применимость:
# Паттерн можно часто встретить в Python-коде, особенно там, где требуется конвертация разных типов данных или
# совместная работа классов с разными интерфейсами.
#
# Признаки применения паттерна:
# Адаптер получает конвертируемый объект в конструкторе или через параметры своих методов.
# Методы Адаптера обычно совместимы с интерфейсом одного объекта. Они делегируют вызовы вложенному объекту,
# превратив перед этим параметры вызова в формат, поддерживаемый вложенным объектом.

import json

import xmltodict


class Target:
    """
    Целевой класс объявляет интерфейс, с которым может работать клиентский код.
    В данном случае - возвращает JSON-объект.
    """

    def request(self) -> dict:
        return {"json_data": {"some_critical_data": "very_much_business_value"}}


class Adaptee:
    """
    Адаптируемый класс содержит некоторое полезное поведение, но его интерфейс несовместим с существующим клиентским
    кодом. Адаптируемый класс нуждается в некоторой доработке, прежде чем клиентский код сможет его использовать.
    В данном случае - возвращает XML-байтстроку.
    """

    def specific_request(self) -> bytes:
        return b"<xml_data><some_critical_data>very_much_business_value</some_critical_data></xml_data>"


class Adapter(Target, Adaptee):
    """
    Адаптер делает интерфейс Адаптируемого класса совместимым с целевым
    интерфейсом благодаря множественному наследованию.
    В данном случае, конвертирует XML-байтстроку в JSON-объект.
    """

    def request(self) -> dict:
        return json.loads(json.dumps(xmltodict.parse(self.specific_request())))


def client_code(target: "Target") -> None:
    """
    Клиентский код поддерживает все классы, использующие интерфейс Target,
    и проверяет формат данных на соответствие ожидаемому.
    """

    data = target.request()
    assert isinstance(data, dict), "Unsupported data format!"
    print(data, end="")


if __name__ == "__main__":
    print("Client works fine with Target interface:")
    target_service = Target()
    client_code(target=target_service)
    print("\n")

    print("Client could not work with Adaptee interface:")
    adaptee_service = Adaptee()
    try:
        client_code(target=adaptee_service)
    except AttributeError:
        print("Adaptee doesn't have 'request' method", end="")
    print("\n")

    print("But client could work with Adaptee service using Adapter:")
    adapted_service = Adapter()
    client_code(target=adapted_service)
