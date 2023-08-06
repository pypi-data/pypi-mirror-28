.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/rm.svg
	:target: https://pypi.org/pypi/rm

.. image:: https://img.shields.io/pypi/v/rm.svg
	:target: https://pypi.org/pypi/rm

|

.. image:: https://api.codacy.com/project/badge/Grade/59291adefe0b4daeb39f5a3f5666f273
	:target: https://www.codacy.com/app/russianidiot/rm-py

.. image:: https://codeclimate.com/github/russianidiot/rm.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/rm.py

.. image:: https://landscape.io/github/russianidiot/rm.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/rm.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/rm.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/rm.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install rm`




Features
````````

- **dirs** and **files** supported
- **~**, **..**, **.** expand
- **no exception** if path not exists



Usage
`````


.. code:: python

	>>> from rm import rm
	
	>>> rm(path)



Examples
````````


.. code:: python

	>>> rm("path/to/file")
	>>> rm("path/to/dir")
	>>> rm("not-existing") # no exception





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/rm.py.svg
	:target: https://github.com/russianidiot/rm.py/issues

