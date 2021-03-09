# Декоратор
**Также известен как:** Обёртка (Wrapper)

## Суть паттерна
**Декоратор** — это структурный паттерн проектирования, который позволяет динамически добавлять объектам новую функциональность, оборачивая их в полезные «обёртки».

## Описание паттерна
Наследование — это первое, что приходит в голову многим программистам, когда нужно расширить какое-то существующее поведение. Но механизм наследования имеет несколько досадных проблем.

- Он статичен. Вы не можете изменить поведение существующего объекта. Для этого вам надо создать новый объект, выбрав другой подкласс.
- Он не разрешает наследовать поведение нескольких классов одновременно. Из-за этого вам приходится создавать множество подклассов-комбинаций для получения совмещённого поведения.

Одним из способов обойти эти проблемы является замена наследования агрегацией либо композицией. Это когда один объект содержит ссылку на другой и делегирует ему работу, вместо того чтобы самому наследовать его поведение. Как раз на этом принципе построен паттерн Декоратор.

Декоратор имеет альтернативное название — *обёртка*. Оно более точно описывает суть паттерна: вы помещаете целевой объект в другой объект-обёртку, который запускает базовое поведение объекта, а затем добавляет к результату что-то своё.

Оба объекта имеют общий интерфейс, поэтому для пользователя нет никакой разницы, с каким объектом работать — чистым или обёрнутым. Вы можете использовать несколько разных обёрток одновременно — результат будет иметь объединённое поведение всех обёрток сразу.

## Применимость
**Когда вам нужно добавлять обязанности объектам на лету, незаметно для кода, который их использует.**</br>
Объекты помещают в обёртки, имеющие дополнительные поведения. Обёртки и сами объекты имеют одинаковый интерфейс, поэтому клиентам без разницы, с чем работать — с обычным объектом данных или с обёрнутым.

**Когда нельзя расширить обязанности объекта с помощью наследования.**</br>
Во многих языках программирования есть ключевое слово final, которое может заблокировать наследование класса. Расширить такие классы можно только с помощью Декоратора.

## Шаги реализации
1) Убедитесь, что в вашей задаче есть один основной компонент и несколько опциональных дополнений или надстроек над ним.
2) Создайте интерфейс компонента, который описывал бы общие методы как для основного компонента, так и для его дополнений.
3) Создайте класс конкретного компонента и поместите в него основную бизнес-логику.
4) Создайте базовый класс декораторов. Он должен иметь поле для хранения ссылки на вложенный объект-компонент. Все методы базового декоратора должны делегировать действие вложенному объекту.
5) И конкретный компонент, и базовый декоратор должны следовать одному и тому же интерфейсу компонента.
6) Теперь создайте классы конкретных декораторов, наследуя их от базового декоратора. Конкретный декоратор должен выполнять свою добавочную функцию, а затем (или перед этим) вызывать эту же операцию обёрнутого объекта.
7) Клиент берёт на себя ответственность за конфигурацию и порядок обёртывания объектов.

## Преимущества и недостатки
**Плюсы:**
1) Большая гибкость, чем у наследования.
2) Позволяет добавлять обязанности на лету.
3) Можно добавлять несколько новых обязанностей сразу.
4) Позволяет иметь несколько мелких объектов вместо одного объекта на все случаи жизни.

**Минусы:**
1) Трудно конфигурировать многократно обёрнутые объекты.
2) Обилие крошечных классов.