.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/formatclass.svg
	:target: https://pypi.org/pypi/formatclass

.. image:: https://img.shields.io/pypi/v/formatclass.svg
	:target: https://pypi.org/pypi/formatclass

|

.. image:: https://api.codacy.com/project/badge/Grade/03a5e45d1d03438cad6b4f74432eb743
	:target: https://www.codacy.com/app/russianidiot/formatclass-py

.. image:: https://codeclimate.com/github/russianidiot/formatclass.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/formatclass.py

.. image:: https://landscape.io/github/russianidiot/formatclass.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/formatclass.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/formatclass.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/formatclass.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install formatclass`





Usage
`````


.. code:: python

	>>> from formatclass import formatclass
	
	>>> formatclass(cls)



Examples
````````


.. code:: python

	>>> class Cls(object): pass
	>>> class Cls2(Cls): 
	    def __init__(self,arg,arg2="default"): pass
	
	# default
	>>> formatclass(CLS2)
	'Cls2(__main__.Cls)(arg, arg2="default")'
	
	# args - False/True (default True)
	>>> formatclass(CLS2,args=False)
	'Cls2(__main__.Cls)'
	
	# fullname - False/True (default True)
	>>> formatclass(CLS2,fullname=False)
	'Cls2(Cls)(arg, arg2="default")'





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/formatclass.py.svg
	:target: https://github.com/russianidiot/formatclass.py/issues

