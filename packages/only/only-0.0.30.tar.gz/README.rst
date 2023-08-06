.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/only.svg
	:target: https://pypi.org/pypi/only

.. image:: https://img.shields.io/pypi/v/only.svg
	:target: https://pypi.org/pypi/only

|

.. image:: https://api.codacy.com/project/badge/Grade/fe6a6f03f9354ae391a907cdff85e47b
	:target: https://www.codacy.com/app/russianidiot/only-py

.. image:: https://codeclimate.com/github/russianidiot/only.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/only.py

.. image:: https://landscape.io/github/russianidiot/only.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/only.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/only.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/only.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install only`





Usage
`````


.. code:: python

	>>> import only
	
	>>> @only.linux
	>>> @only.osx
	>>> @only.unix
	>>> @only.windows



Examples
````````


.. code:: python

	>>> @only.osx
	>>> def osascript(): pass
	
	>>> osascript() # raise OSError if not OS X





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/only.py.svg
	:target: https://github.com/russianidiot/only.py/issues

