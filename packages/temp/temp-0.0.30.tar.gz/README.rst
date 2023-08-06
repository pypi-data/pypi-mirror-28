.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/temp.svg
	:target: https://pypi.org/pypi/temp

.. image:: https://img.shields.io/pypi/v/temp.svg
	:target: https://pypi.org/pypi/temp

|

.. image:: https://api.codacy.com/project/badge/Grade/58d851db667e4e21af9d7381b365a1c3
	:target: https://www.codacy.com/app/russianidiot/temp-py

.. image:: https://codeclimate.com/github/russianidiot/temp.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/temp.py

.. image:: https://landscape.io/github/russianidiot/temp.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/temp.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/temp.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/temp.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install temp`





Usage
`````


.. code:: python

	>>> from temp import tempdir, tempfile, TMPDIR
	
	>>> tempdir() # dir
	>>> tempfile() # file



Examples
````````


.. code:: python

	>>> tempdir() # dir
	'/var/folders/rv/gy6_gnfs1d7_pd1518p27tsr0000gn/T/tmpqlLDxb'
	
	>>> tempfile() # file
	'/var/folders/rv/gy6_gnfs1d7_pd1518p27tsr0000gn/T/tmpsctFHJ'
	
	>>> TMPDIR
	'/var/folders/rv/gy6_gnfs1d7_pd1518p27tsr0000gn/T'





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/temp.py.svg
	:target: https://github.com/russianidiot/temp.py/issues

