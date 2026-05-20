# Auto Shop App

Flask application for managing an auto service shop.

## Features

- manages clients;
- stores client cars;
- creates repair and service orders;
- assigns services, parts, and employees to orders;
- completes orders with automatic total calculation;
- shows order lists and business statistics.

## Dependencies

Install dependencies:

```powershell
pip install -r requirements.txt
```

The app uses Python's built-in `sqlite3` module, so no external database driver is required.

## Database

The SQLite schema and seed data are stored in:

```text
auto_shop_app/schema.sql
```

By default, the app creates this database on first use:

```text
auto_shop_app/auto_shop.sqlite3
```

To use a different database file, set `AUTO_SHOP_DB` before starting the app:

```powershell
$env:AUTO_SHOP_DB = "C:\path\to\auto_shop.sqlite3"
py app.py
```

To rebuild a database manually:

```powershell
sqlite3 auto_shop_app/auto_shop.sqlite3 ".read auto_shop_app/schema.sql"
```

## Run

Run from the source tree:

```powershell
py app.py
```

The app will be available at:

```text
http://127.0.0.1:5000
```

After package installation, the command is also available:

```powershell
auto-shop-app
```

## Build

Build wheel and source distribution:

```powershell
py -m build
```

Artifacts are written to `dist/`.

Build HTML documentation:

```powershell
py setup.py build_sphinx
```

The generated documentation is written to `docs/_build/html`.
