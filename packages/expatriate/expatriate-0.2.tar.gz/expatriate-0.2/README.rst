expatriate
==========
.. image:: https://travis-ci.org/cjaymes/expatriate.svg?branch=master
.. image:: https://readthedocs.org/projects/expatriate/badge/?version=latest

XML parsing and generation library on top of expat with Python object mapping
(ORM). See tests/fixtures for examples of how to use.

Install (system-wide):

    pip install expatriate

Install (using venv):

    python3 -m venv venv
    . venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python3 setup.py install

Tests:

    pip install pytest
    pytest
