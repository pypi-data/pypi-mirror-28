.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/shebang.svg
	:target: https://pypi.org/pypi/shebang

.. image:: https://img.shields.io/pypi/v/shebang.svg
	:target: https://pypi.org/pypi/shebang

|

.. image:: https://api.codacy.com/project/badge/Grade/d6ba7ecf67b24670b17d56b4d5d5ded4
	:target: https://www.codacy.com/app/russianidiot/shebang-py

.. image:: https://codeclimate.com/github/russianidiot/shebang.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/shebang.py

.. image:: https://landscape.io/github/russianidiot/shebang.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/shebang.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/shebang.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/shebang.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install shebang`





Usage
`````


.. code:: python

	>>> from shebang import shebang
	
	>>> shebang(path)



Examples
````````


.. code:: python

	>>> shebang("path/to/file.py")
	'/usr/bin/env python'
	
	>>> shebang("path/to/file.txt")
	None
	
	shebang("/bin/test")
	None





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/shebang.py.svg
	:target: https://github.com/russianidiot/shebang.py/issues

