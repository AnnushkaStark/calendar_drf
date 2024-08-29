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

* Установите зависимости:

  docker-compose run --rm web pip install -r requirements.txt

* Сгенерируйте миграции:

  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate

* Запустите сервер и Redis:

  docker-compose up



# Оптимизация работы базы данных

* Изменена модель события -     добавлено поле DatetimeField - дата окончания повторов события

* Добалена модель для хранения списка дат повторения событи
* Добавлена модель связи M2M событие с датой повторения

* Убраны задачи селери

## изменение логики работы эндпойнта получения событий за опрделенную дату

* Используется запрос который получает из модели все события от текущей даты, до даты выбранной пользоватлем, если дата выбранная пользователем больше текущий, если дата выбранная пользователм меньше текущей, то будут выбраны только события от выбранной даты до текущей, а если выбранная дата равна текущей, то только за выбранную дату - это позволяет сократить количество данных выбраннных для дальнейшей обработки

## Изменение логики работы удаления события за выбранную дату
* Удаляется не само событие а дата его повтора в этот день, если у события нет повторов удалиться само события

## Изменение логики работы удаления всех повторов от выбранного события
* Используется фильтрация дат повторов события с удалением всех дат повторений от выбранной даты? если у события нет поатовров так же будет удалено само событие

## Во всех эндпойнтах изменена логика выборки события по дате и ID 
* Дата начала события может быть как датой его начала, так и датой его      повтора

## Дополниетельно добален эндпойнт полного удаления события
 *  Если нужно удалить объект полностью просто удаление по ID

## Создан дополнительный сериалайзер для создание и обновления событий
 * В серилайзер добавлена дополнительно валидация, чтобы у событий с периодичностью  дата окочания пераода повторений была обязательным параметром

Таким образом  мы создаем и сохраняем только одно событие, вся логика повторов события перенесена в список дат в которые это событие может повторяться.

