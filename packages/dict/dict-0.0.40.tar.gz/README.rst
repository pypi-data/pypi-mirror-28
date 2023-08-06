.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/dict.svg
	:target: https://pypi.org/pypi/dict

.. image:: https://img.shields.io/pypi/v/dict.svg
	:target: https://pypi.org/pypi/dict

|

.. image:: https://api.codacy.com/project/badge/Grade/60d350ee07c74bd181d23b2f3c9e7430
	:target: https://www.codacy.com/app/russianidiot/dict-py

.. image:: https://codeclimate.com/github/russianidiot/dict.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/dict.py

.. image:: https://landscape.io/github/russianidiot/dict.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/dict.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/dict.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/dict.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install dict`




Features
````````


*	**attribute-style access**
* 	**None** instead of **KeyError**
* 	safe **remove**
* 	jQuery like **methods chaining**



Usage
`````


.. code:: python

	>>> from dict import dict



Examples
````````


.. code:: python

	>>> dict(k="v")["k"]
	"v"
	
	>>>  dict(k="v").k
	"v"
	
	>>> dict(k="v")["not_existing"]
	None
	
	>>> dict(k="v").not_existing
	None
	
	>>> dict(k="v").get("K",i=True) # case insensitive





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/dict.py.svg
	:target: https://github.com/russianidiot/dict.py/issues

