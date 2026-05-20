Auto Shop App
=============

Auto Shop App is a Flask web application for managing an auto service shop.

Features
--------

* client management;
* client car management;
* repair and service order creation;
* service, part, and employee assignment;
* order completion with total price calculation;
* order list view;
* revenue, parts, services, clients, and employees statistics.

Project Structure
-----------------

``app.py``
   Entry point for running the application from the source tree.

``auto_shop_app/``
   Python package with Flask application code and HTML templates.

``pyproject.toml``
   Setuptools package build configuration.

``setup.py``
   Setuptools integration for the Sphinx ``build_sphinx`` command.

``requirements.txt``
   Runtime, build, and documentation dependencies.

Build Commands
--------------

Install dependencies:

.. code-block:: powershell

   pip install -r requirements.txt

Run the application:

.. code-block:: powershell

   python app.py

Build the Python package:

.. code-block:: powershell

   python -m build

Build this documentation through Setuptools:

.. code-block:: powershell

   python setup.py build_sphinx

Application Module
------------------

.. automodule:: auto_shop_app.app
   :members:
   :undoc-members:
