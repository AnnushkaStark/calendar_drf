# Teстовое задание DRF

Создать простой аналог гугл-календаря, используя Django
Шаги по запуску и сборке должны быть описаны в readme проекта. Для работы необходимо использовать 8000 порт от локалхоста

## Сервис должен реализовывать следующие запросы:

* POST  add/ - Добавить событие со следующими параметрами в виде json:

  1. name [str] — название события
  2. start_at [int, unix timestamp в секундах (UTC)] —  время и дата начала события
  3. period [int | None] — как часто должно повторяться событие (например, при period = 7 событие будет повторяться каждую неделю)
Возвращается json с полем id — уникальный id первого созданного события

*  POST  remove/{id}/{year}/{month}/{day}/

    Удалить конкретное событие по его id (как и в гугл-календаре: нужно удалить только ТЕКУЩЕЕ событие, а не все события из цепочки повторения)

*  POST  remove-next/{id}/{year}/{month}/{day}/

    Удалить конкретное событие по его id и все последующие по цепочке

* POST  update/{id}/{year}/{month}/{day}/

    Изменить название конкретного события по его id (как и в гугл-календаре: нужно изменить только ТЕКУЩЕЕ событие, а не все события из цепочки повторения). 
    Параметры в виде json:
    name [str] — новое название события

* GET  events/{year}/{month}/{day}/

  Получить в ответ список событий в указанный день (в списке указывать name и id события)

# Запуск проекта
