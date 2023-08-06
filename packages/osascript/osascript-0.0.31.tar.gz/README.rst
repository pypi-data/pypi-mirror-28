.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/osascript.svg
	:target: https://pypi.org/pypi/osascript

.. image:: https://img.shields.io/pypi/v/osascript.svg
	:target: https://pypi.org/pypi/osascript

|

.. image:: https://api.codacy.com/project/badge/Grade/0602d537ebdd4a059139afbf07b43fc5
	:target: https://www.codacy.com/app/russianidiot/osascript-py

.. image:: https://codeclimate.com/github/russianidiot/osascript.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/osascript.py

.. image:: https://landscape.io/github/russianidiot/osascript.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/osascript.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/osascript.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/osascript.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install osascript`





Usage
`````


.. code:: python

	>>> from osascript import osascript
	
	>>> returncode,stdout,stderr = osascript(code)



Examples
````````


.. code:: python

	>>> returncode,stdout,stderr = osascript('display dialog "42"')





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/osascript.py.svg
	:target: https://github.com/russianidiot/osascript.py/issues

