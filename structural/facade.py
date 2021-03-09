# Применимость:
# Паттерн часто встречается в клиентских приложениях, написанных на Python, которые используют классы-фасады
# для упрощения работы со сложными библиотеки или API.
#
# Признаки применения паттерна:
# Фасад угадывается в классе, который имеет простой интерфейс, но делегирует основную часть работы другим классам.
# Чаще всего, фасады сами следят за жизненным циклом объектов сложной системы.


class AWSFacade:
    """
    Класс Фасада предоставляет простой интерфейс для сложной логики одной или нескольких подсистем.
    Фасад делегирует запросы клиентов соответствующим объектам внутри подсистемы.
    Фасад также отвечает за управление их жизненным циклом.
    Все это защищает клиента от нежелательной сложности подсистемы.
    """

    def __init__(self, db_subsystem: "DbSubsystem", iot_subsystem: "IoTSubsystem") -> None:
        self.db_subsystem = db_subsystem or DbSubsystem()
        self.iot_subsystem = iot_subsystem or IoTSubsystem()

    def initialize_charger(self) -> str:
        results = [
            self.iot_subsystem.create_thing(),
            self.iot_subsystem.add_shadow_to_thing(),
            self.db_subsystem.check_charger_in_shadow_table(),
            self.db_subsystem.check_charger_in_cloud_table(),
            self.db_subsystem.check_charger_in_es()
        ]
        return f"Charger initialized:\n{''.join(results)}"


class DbSubsystem:
    """
    Подсистема может принимать запросы либо от фасада, либо от клиента напрямую.
    В любом случае, для Подсистемы Фасад – это ещё один клиент, и он не является
    частью Подсистемы.
    """

    @staticmethod
    def check_charger_in_shadow_table():
        return "Charger got to shadow table!\n"

    @staticmethod
    def check_charger_in_cloud_table():
        return "Charger got to cloud table!\n"

    @staticmethod
    def check_charger_in_es():
        return "Charger got to UI!\n"


class IoTSubsystem:
    """
    Некоторые фасады могут работать с разными подсистемами одновременно.
    """

    @staticmethod
    def create_thing():
        return "Charger's thing is created!\n"

    @staticmethod
    def add_shadow_to_thing():
        return "Shadow added to charger's thing!\n"


def client_code(aws_facade: AWSFacade) -> None:
    """
    Клиентский код работает со сложными подсистемами через простой интерфейс, предоставляемый Фасадом.
    Когда фасад управляет жизненным циклом подсистемы, клиент может даже не знать о существовании подсистемы.
    Такой подход позволяет держать сложность под контролем.
    """

    print(aws_facade.initialize_charger(), end="")


if __name__ == "__main__":
    # В клиентском коде могут быть уже созданы некоторые объекты подсистемы.
    # В этом случае может оказаться целесообразным инициализировать Фасад с этими объектами вместо того,
    # чтобы позволить Фасаду создавать новые экземпляры.

    db = DbSubsystem()
    iot = IoTSubsystem()
    facade = AWSFacade(db_subsystem=db, iot_subsystem=iot)
    client_code(aws_facade=facade)
