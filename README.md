# Auto Shop App

Веб-приложение для управления автосервисом.

## Что умеет

- вести список клиентов;
- добавлять автомобили клиентов;
- создавать заказы на ремонт или обслуживание;
- выбирать услуги, запчасти и сотрудников для заказа;
- завершать заказ с расчетом итоговой суммы;
- показывать список заказов;
- показывать статистику по выручке, клиентам, услугам, запчастям и сотрудникам.

## Технологии

- Python
- Flask
- PostgreSQL
- psycopg2

## Установка

Создайте виртуальное окружение и установите зависимости:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## База данных

Приложение подключается к PostgreSQL по строке из `app.py`:

```python
postgresql://postgres:2006@localhost/car_service
```

Перед запуском нужна база `car_service` с таблицами и данными. Файл `dataset.sql` в репозитории является дампом PostgreSQL в custom/binary формате `pg_dump`, поэтому его нужно восстанавливать через `pg_restore`, например:

```powershell
createdb -U postgres car_service
pg_restore -U postgres -d car_service dataset.sql
```

## Запуск

```powershell
python app.py
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:5000
```

Также после установки пакета доступна команда:

```powershell
auto-shop-app
```

## Сборка пакета

Проект настроен для сборки через `setuptools` и `pyproject.toml`.

Установите зависимости для сборки:

```powershell
pip install -r requirements.txt
```

Соберите wheel и sdist:

```powershell
python -m build
```

Готовые артефакты появятся в папке `dist/`.

Локальная установка проекта:

```powershell
pip install .
```

## Структура

- `app.py` - файл запуска приложения из исходников;
- `auto_shop_app/` - Python-пакет приложения с Flask-кодом и HTML-шаблонами;
- `pyproject.toml` - настройки сборки через setuptools;
- `dataset.sql` - экспорт базы PostgreSQL;
- `requirements.txt` - зависимости Python.
