.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/stdin.svg
	:target: https://pypi.org/pypi/stdin

.. image:: https://img.shields.io/pypi/v/stdin.svg
	:target: https://pypi.org/pypi/stdin

|

.. image:: https://api.codacy.com/project/badge/Grade/8dd159f87e8b4662a3905e59ae14acce
	:target: https://www.codacy.com/app/russianidiot/stdin-py

.. image:: https://codeclimate.com/github/russianidiot/stdin.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/stdin.py

.. image:: https://landscape.io/github/russianidiot/stdin.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/stdin.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/stdin.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/stdin.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install stdin`





Usage
`````


.. code:: python

	>>> from stdin import STDIN



Examples
````````


.. code:: bash

	$ echo "stdin text" | python -c "import stdin;print(stdin.STDIN)"
	stdin text
	
	$ python -c "import stdin;print(stdin.STDIN)"
	None





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/stdin.py.svg
	:target: https://github.com/russianidiot/stdin.py/issues

