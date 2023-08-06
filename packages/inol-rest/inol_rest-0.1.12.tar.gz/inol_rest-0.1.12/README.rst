inol_rest
=========

.. image:: https://circleci.com/gh/awalker125/inol_rest.svg?style=shield
    :target: https://circleci.com/gh/awalker125/inol_rest
    :alt: CI Status

.. image:: https://codecov.io/gh/awalker125/inol_rest/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/awalker125/inol_rest
    :alt: Code Coverage

.. image:: https://badge.fury.io/py/inol_rest.svg
    :target: https://badge.fury.io/py/inol_rest
    :alt: PyPi PAckage



Requirements.
-------------

Python 2.7 and 3.4+

Installation & Usage
--------------------

.. code:: bash

	pip install inol_rest



## building

.. code-block:: bash

   cd inol_rest/src/inol_rest/static
   gulp

## running locally

.. code-block:: bash

   cd inol_rest/
   . ./setup_shell.sh
   cd src
   ./manage.py runserver


This is a microservice responsible for doing all of the inol calculations


curl
----

.. code-block:: bash

   curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'X-Fields: inol' -d '{ \ 
   "max": 100, \ 
   "reps": 1, \ 
   "weight": 100 \ 
   }' 'http://127.0.0.1:5000/api/inol/'


Author
------

* awalker125
