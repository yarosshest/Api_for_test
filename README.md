# Api_for_test 
Реализация серверной части api для 5 семестра МИРЭА


# !!! Загрузите сырые данные !!!


**Загрузите сырые данные** https://disk.yandex.ru/d/HDpkfG1onHU5tw **и поместите их папку** [parsing](database%2Fparsing)

## Запуск

- [api-compose.yml](api-compose.yml) - для запуска api

Для запуска проекта необходимо выполнить команду:
bash
docker-compose -f "название контейнера" build
docker-compose -f "название контейнера" up


api будет доступно по адресу: http://localhost:60106

## Реализация

### База данных

Для хранения данных была выбрана база данных PostgreSQL, и python библиотека для работы с ней SQLAlchemy.

Как тестовая база данных была взята база данных кинопоиска, из которой были взяты фильмы с дополнительным коротким
описанием ~ 11000 фильмов.

Все модели описаны в файле [Db_objects.py](database%2FDb_objects.py)

### Логика работы

Логика работы рекомендательной системы описана в [async_db.py](database%2Fasync_db.py)

Здесь реализованна логика работы с базой данных, а так же логика работы с рекомендательной системой.
Все выполнено в SQLAlchemy в асинхронном режиме.

Работа с базой данных выполнена через обращения к статичным методам класса asyncHandler.

При каждом вызове функции, которая обращается к базе данных, происходит подключение к базе данных, через декоратор
@Session и после выполнения функции, происходит отключение от базы данных.

### Docker

Для запуска проекта в docker контейнере, были написаны два Docker-compose файла:
- [api-compose.yml](api-compose.yml) - для запуска api

В них происходит запуск контейнера с базой данных, а так же контейнера с api или ботом.

## Документация

Документация к api находиться по адресу http://localhost:60106/docs (более полная и интерактивная) или
в файле [doc.md](api%2Fdoc.md)