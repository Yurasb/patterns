# Применимость:
# Паттерн можно часто встретить в Python-коде, особенно в коде, работающем с потоками данных.
#
# Признаки применения паттерна:
# Декоратор можно распознать по создающим методам, которые принимают в параметрах объекты того же абстрактного типа
# или интерфейса, что и текущий класс.


from abc import ABC, abstractmethod


class DataReporter(ABC):
    """
    Базовый компонент определяет поведение, которое изменяется декораторами.
    """

    @abstractmethod
    def report_data(self) -> str:
        pass


class BasicSessionDataReporter(DataReporter):
    """
    Конкретные реализации базового компонента предоставляют реализации поведения по умолчанию.
    Может быть несколько вариаций этих классов.
    """

    def report_data(self) -> str:
        return "I'm reporting basic charging session data to device' shadow"


class BasicReporterDecorator(DataReporter):
    """
    Базовый класс Декоратора следует тому же интерфейсу, что и другие компоненты.
    Основная цель этого класса - определить интерфейс обёртки для всех конкретных декораторов.
    Реализация кода обёртки по умолчанию может включать в себя поле для хранения завёрнутого компонента и средства его
    инициализации.
    """

    _reporter: DataReporter = None

    def __init__(self, reporter: "DataReporter") -> None:
        self._reporter = reporter

    @property
    def reporter(self) -> DataReporter:
        """
        Декоратор делегирует всю работу обёрнутому компоненту.
        """

        return self._reporter

    def report_data(self) -> str:
        return self._reporter.report_data()


class ShadowReporterDecorator(BasicReporterDecorator):
    """
    Конкретные Декораторы вызывают обёрнутый объект и изменяют его результат
    некоторым образом.
    """

    def report_data(self) -> str:
        """
        Декораторы могут вызывать родительскую реализацию операции, вместо вызова обёрнутого объекта напрямую.
        Такой подход упрощает расширение классов декораторов.
        """

        return f"{self.reporter.report_data()} and added meter values to device' shadow"


class MQTTReporterDecorator(BasicReporterDecorator):
    """
    Декораторы могут выполнять своё поведение до или после вызова обёрнутого объекта.
    """
    _mqtt_client: str = None

    def setup_mqtt_client(self) -> str:
        self._mqtt_client = "MQTT Client up"
        return "MQTT Client is set up."

    def teardown_mqtt_client(self) -> str:
        self._mqtt_client = "MQTT Client down"
        return "MQTT Client is teared down."

    def report_data(self) -> str:
        self.setup_mqtt_client()
        reported = f"{self.reporter.report_data()} and sent meter values to MQTT topic"
        self.teardown_mqtt_client()
        return reported


def client_code(component: "DataReporter") -> None:
    """
    Клиентский код работает со всеми объектами, используя интерфейс Компонента.
    Таким образом, он остаётся независимым от конкретных классов компонентов, с
    которыми работает.
    """

    print(f"RESULT: {component.report_data()}", end="")


if __name__ == "__main__":
    # Таким образом, клиентский код может поддерживать как простые компоненты...
    just_basic_data = BasicSessionDataReporter()
    print("Client: I've got a simple component:")
    client_code(just_basic_data)
    print("\n")

    # ...так и декорированные.
    #
    # Обратите внимание, что декораторы могут обёртывать не только простые
    # компоненты, но и другие декораторы.
    with_meter_values_to_shadow = ShadowReporterDecorator(just_basic_data)
    with_meter_values_to_mqtt = MQTTReporterDecorator(with_meter_values_to_shadow)
    print("Client: Now I've got a decorated component:")
    client_code(with_meter_values_to_mqtt)
