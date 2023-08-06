.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/cached.svg
	:target: https://pypi.org/pypi/cached

.. image:: https://img.shields.io/pypi/v/cached.svg
	:target: https://pypi.org/pypi/cached

|

.. image:: https://api.codacy.com/project/badge/Grade/cfa863da31c84f0bab4065f12dc3f061
	:target: https://www.codacy.com/app/russianidiot/cached-py

.. image:: https://codeclimate.com/github/russianidiot/cached.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/cached.py

.. image:: https://landscape.io/github/russianidiot/cached.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/cached.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/cached.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/cached.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install cached`





Usage
`````


.. code:: python

	>>> from cached import cached
	
	>>> cached(func)()



Examples
````````


.. code:: python

	>>> def func(*args,**kwags):
		print('log')
		return "result"
	
	>>> cached(func)()
	log
	'result'
	>>> cached(func)() # cached :)
	'result'





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/cached.py.svg
	:target: https://github.com/russianidiot/cached.py/issues

