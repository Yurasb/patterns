# Применимость:
# Паттерн Компоновщик встречается в любых задачах, которые связаны с построением дерева. Самый простой пример —
# составные элементы GUI, которые тоже можно рассматривать как дерево.
#
# Признаки применения паттерна:
# Если из объектов строится древовидная структура, и со всеми объектами дерева, как и с самим деревом работают через
# общий интерфейс.

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Loader(ABC):
    """
    Базовый класс "компонент" объявляет общие операции как для простых, так и для сложных объектов структуры.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def parent(self) -> Loader:
        return self._parent

    @parent.setter
    def parent(self, parent: "Loader"):
        """
        При необходимости базовый класс может объявить интерфейс для установки и получения родителя компонента в
        древовидной структуре. Он также может предоставить некоторую реализацию по умолчанию для этих методов.
        """

        self._parent = parent

    # В некоторых случаях целесообразно определить операции управления потомками прямо в базовом классе.
    # Таким образом, вам не нужно будет предоставлять конкретные классы компонентов клиентскому коду, даже во время
    # сборки дерева объектов.
    # Недостаток такого подхода в том, что эти методы будут пустыми для компонентов уровня "листа".

    def add_node(self, component: "Loader") -> None:
        pass

    def remove_node(self, component: "Loader") -> None:
        pass

    def is_composite(self) -> bool:
        """
        Можно предоставить метод, который позволит клиентскому коду понять, может ли компонент иметь вложенные объекты.
        """

        return False

    @abstractmethod
    def start_load(self) -> str:
        """
        Базовый класс может сам реализовать некоторое поведение по умолчанию или поручить это конкретным классам,
        объявив метод, содержащий поведение абстрактным.
        """

        pass

    @abstractmethod
    def stop_load(self) -> str:
        pass


class LoadNode(Loader):
    """
    Класс уровня "лист" представляет собой конечные объекты структуры. Лист не может иметь вложенных компонентов.
    Обычно объекты Листьев выполняют фактическую работу, тогда как объекты уровня "узел" лишь делегируют работу
    своим подкомпонентам.
    """

    def start_load(self) -> str:
        return f"{self.name} started load.\n"

    def stop_load(self) -> str:
        return f"{self.name} stopped load.\n"


class LoadCluster(Loader):
    """
    Класс "узел" / "контейнер" содержит сложные компоненты, которые могут иметь вложенные компоненты.
    Обычно объекты Контейнеры делегируют фактическую работу своим детям, а затем «суммируют» результат.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self._children: List[Loader] = []
        super().__init__(name)

    def add_node(self, component: "Loader") -> None:
        """
        Объект контейнера может как добавлять компоненты в свой список вложенных
        компонентов, так и удалять их, как простые, так и сложные.
        """
        self._children.append(component)
        component.parent = self

    def remove_node(self, component: "Loader") -> None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def start_load(self) -> str:
        """
        Контейнер выполняет свою основную логику особым образом. Он проходит рекурсивно через всех своих детей,
        собирая и суммируя их результаты.
        Поскольку потомки контейнера передают эти вызовы своим потомкам и так далее, в результате
        обходится всё дерево объектов.
        """
        results = []
        for child in self._children:
            results.append(child.start_load())
        return f"Cluster {self.name} started load:\n{''.join(results)}"

    def stop_load(self) -> str:
        results = []
        for child in self._children:
            results.append(child.stop_load())
        return f"Cluster {self.name} stopped load:\n{''.join(results)}"


def client_code(loader: "Loader") -> None:
    """
    Клиентский код работает со всеми компонентами через базовый интерфейс.
    """

    print(loader.start_load())
    print(loader.stop_load())


def client_code2(loader1: "Loader", loader2: "Loader") -> None:
    """
    Благодаря тому, что операции управления потомками объявлены в базовом классе Компонента,
    клиентский код может работать как с простыми, так и со сложными компонентами, вне зависимости от их
    конкретных классов.
    """

    if loader1.is_composite():
        loader1.add_node(loader2)

    print(loader1.start_load())
    print(loader1.stop_load())


if __name__ == "__main__":
    # Таким образом, клиентский код может поддерживать простые компоненты - листья
    simple_loader = LoadNode("Simple load node")
    client_code(loader=simple_loader)

    # ... а также сложные контейнеры
    master_loader = LoadCluster("Master Loader")
    client_code2(loader1=master_loader, loader2=simple_loader)

    # Можно создать более сложную структуру и управлять ею через единый интерфейс:
    # 1) создаём "узлы" / "контейнеры"
    session_load_cluster = LoadCluster("Session load cluster")
    faults_load_cluster = LoadCluster("Faults load cluster")

    # 2) заполняем контейнеры "листьями"
    session_load_cluster.add_node(LoadNode("Session load node 1"))
    session_load_cluster.add_node(LoadNode("Session load node 2"))
    faults_load_cluster.add_node(LoadNode("Faults load node 1"))
    faults_load_cluster.add_node(LoadNode("Faults load node 2"))

    # 3) добавляем заполненные контейнеры в корневой "узел" / "контейнер"
    master_loader.add_node(session_load_cluster)
    master_loader.add_node(faults_load_cluster)

    # 4) управляем всей структурой только через интерфейс корневого компонента
    print(master_loader.start_load())
    print(master_loader.start_load())
