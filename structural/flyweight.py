# Применимость:
# Весь смысл использования Легковеса — в экономии памяти.
# Поэтому, если в приложении нет такой проблемы, то вы вряд ли найдёте там примеры Легковеса.
#
# Признаки применения паттерна:
# Легковес можно определить по создающим методам класса, которые возвращают закешированные объекты,
# вместо создания новых.

import json

from dataclasses import dataclass
from typing import Set, Dict, List


@dataclass
class Flyweight:
    """
    Легковес хранит общую часть состояния (также называемую внутренним состоянием), которая принадлежит нескольким
    реальным бизнес-объектам.
    Легковес принимает оставшуюся часть состояния (внешнее состояние, уникальное для каждого объекта) через его
    параметры метода.
    """

    shared_state: Set

    def operation(self, unique_state: Set) -> None:
        print(f"Flyweight: Displaying shared ({self.shared_state}) and unique ({unique_state}) state.", end="")


class FlyweightFactory:
    """
    Фабрика Легковесов создает объекты-Легковесы и управляет ими. Она обеспечивает правильное разделение легковесов.
    Когда клиент запрашивает легковес, фабрика либо возвращает существующий экземпляр, либо создает новый,
    если он ещё не существует.
    """

    _flyweights: Dict[str, Flyweight] = {}

    def __init__(self, initial_flyweights: List) -> None:
        for state in initial_flyweights:
            self._flyweights[self.get_key(state)] = Flyweight(state)

    @staticmethod
    def get_key(state: Set) -> str:
        """
        Возвращает хеш строки Легковеса для данного состояния.
        """

        return "_".join(state)

    def get_flyweight(self, shared_state: Set) -> Flyweight:
        """
        Возвращает существующий Легковес с заданным состоянием или создает
        новый.
        """

        key = self.get_key(shared_state)

        if not self._flyweights.get(key):
            print("FlyweightFactory: Can't find a flyweight, creating new one.")
            self._flyweights[key] = Flyweight(shared_state)
        else:
            print("FlyweightFactory: Reusing existing flyweight.")

        return self._flyweights[key]

    def list_flyweights(self) -> None:
        count = len(self._flyweights)
        print(f"FlyweightFactory: I have {count} flyweights:")
        print("\n".join(map(str, self._flyweights.keys())), end="")


def add_car_to_police_database(
        factory: "FlyweightFactory",
        plates: str,
        owner: str,
        brand: str,
        model: str,
        color: str
) -> None:
    print("\n\nClient: Adding a car to database.")
    flyweight = factory.get_flyweight({brand, model, color})
    # Клиентский код либо сохраняет, либо вычисляет внешнее состояние и передает
    # его методам легковеса.
    flyweight.operation({plates, owner})


if __name__ == "__main__":
    # Клиентский код обычно создает кучу предварительно заполненных легковесов на этапе инициализации приложения.

    factory = FlyweightFactory([
        {"Chevrolet", "Camaro2018", "pink"},
        {"Mercedes Benz", "C300", "black"},
        {"Mercedes Benz", "C500", "red"},
        {"BMW", "M5", "red"},
        {"BMW", "X6", "white"},
    ])

    factory.list_flyweights()

    add_car_to_police_database(factory, "CL234IR", "James Doe", "BMW", "M5", "red")

    add_car_to_police_database(factory, "CL234IR", "James Doe", "BMW", "X1", "red")

    print("\n")

    factory.list_flyweights()
