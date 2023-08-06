.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/write.svg
	:target: https://pypi.org/pypi/write

.. image:: https://img.shields.io/pypi/v/write.svg
	:target: https://pypi.org/pypi/write

|

.. image:: https://api.codacy.com/project/badge/Grade/075eda6d69fa422f86a26f093ddcf26d
	:target: https://www.codacy.com/app/russianidiot/write-py

.. image:: https://codeclimate.com/github/russianidiot/write.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/write.py

.. image:: https://landscape.io/github/russianidiot/write.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/write.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/write.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/write.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install write`





Usage
`````


.. code:: python

	>>> from write import write
	
	>>> write(path,text)



Examples
````````


.. code:: python

	>>> write(path,'string')
	>>> open(path).read()
	'string'
	
	>>> write(path,None) # touch
	>>> open(path).read()
	''
	
	>>> write(path,42) # write integer
	>>> open(path).read()
	'42'
	
	>>> write(path,dict()) # converted to str
	>>> open(path).read()
	'{}'





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/write.py.svg
	:target: https://github.com/russianidiot/write.py/issues

