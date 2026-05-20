# Auto Shop App

Веб-приложение на Flask для управления автосервисом.

## Возможности

- ведение списка клиентов;
- хранение автомобилей клиентов;
- создание заказов на ремонт и обслуживание;
- выбор услуг, запчастей и сотрудников для заказа;
- завершение заказа с автоматическим расчетом итоговой суммы;
- просмотр списка заказов;
- просмотр статистики по выручке, клиентам, услугам, запчастям и сотрудникам.

## Требования

- `Flask` - веб-фреймворк;
- `build` - сборка Python-пакета;
- `setuptools` и `wheel` - инструменты сборки;
- `Sphinx` - сборка документации.

## Локальный запуск

Перейдите в папку проекта:

```powershell
cd C:\Users\iloveass2\Desktop\auto-shop-app
```

Создайте виртуальное окружение:

```powershell
py -m venv .venv
```

Активируйте окружение:

```powershell
.venv\Scripts\Activate.ps1
```

Если PowerShell запрещает запуск скрипта активации, выполните один раз:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Затем снова активируйте окружение.

Установите зависимости:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Запустите приложение:

```powershell
python app.py
```

Приложение будет доступно по адресу:

```text
http://127.0.0.1:5000
```

Если команда `python` недоступна, попробуйте:

```powershell
py app.py
```

## База данных SQLite

Схема и начальные данные находятся в файле:

```text
auto_shop_app/schema.sql
```

При первом запуске приложение автоматически создает SQLite-базу:

```text
auto_shop_app/auto_shop.sqlite3
```

Файл базы данных не добавляется в Git, потому что он указан в `.gitignore`.

Чтобы использовать другой путь к базе данных, задайте переменную окружения `AUTO_SHOP_DB` перед запуском:

```powershell
$env:AUTO_SHOP_DB = "C:\path\to\auto_shop.sqlite3"
python app.py
```

Пересоздать базу вручную можно командой:

```powershell
sqlite3 auto_shop_app/auto_shop.sqlite3 ".read auto_shop_app/schema.sql"
```

## Переменные окружения

Приложение поддерживает следующие переменные:

| Переменная | Значение по умолчанию | Назначение |
| --- | --- | --- |
| `AUTO_SHOP_DB` | `auto_shop_app/auto_shop.sqlite3` | Путь к файлу SQLite-базы |
| `FLASK_RUN_HOST` | `127.0.0.1` | Хост, на котором запускается Flask |
| `FLASK_RUN_PORT` | `5000` | Порт Flask-приложения |
| `FLASK_DEBUG` | `0` | Режим отладки: `1`, `true` или `yes` включает debug |

Пример запуска на другом порту:

```powershell
$env:FLASK_RUN_PORT = "8080"
python app.py
```

## Запуск через Docker

Соберите Docker-образ:

```powershell
docker build -t auto-shop-app .
```

Запустите контейнер:

```powershell
docker run --rm -p 5000:5000 -v auto-shop-data:/data auto-shop-app
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:5000
```

В Docker база данных по умолчанию хранится здесь:

```text
/data/auto_shop.sqlite3
```

Том `auto-shop-data` нужен, чтобы данные сохранялись после остановки контейнера.

Пример запуска с явными переменными окружения:

```powershell
docker run --rm `
  -p 5000:5000 `
  -v auto-shop-data:/data `
  -e AUTO_SHOP_DB=/data/auto_shop.sqlite3 `
  -e FLASK_RUN_HOST=0.0.0.0 `
  -e FLASK_RUN_PORT=5000 `
  -e FLASK_DEBUG=0 `
  auto-shop-app
```

## Установка как пакет

После установки проекта как Python-пакета будет доступна команда `auto-shop-app`:

```powershell
python -m pip install .
auto-shop-app
```

## Сборка пакета

Сборка wheel и source distribution:

```powershell
python -m build
```

Готовые артефакты появятся в папке:

```text
dist/
```

## Сборка документации

Документация находится в папке `docs/` и собирается через Sphinx.

Собрать HTML-документацию:

```powershell
python setup.py build_sphinx
```

Готовая документация появится в папке:

```text
docs/_build/html
```
