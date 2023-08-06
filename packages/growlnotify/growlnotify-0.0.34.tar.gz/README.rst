.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/growlnotify.svg
	:target: https://pypi.org/pypi/growlnotify

.. image:: https://img.shields.io/pypi/v/growlnotify.svg
	:target: https://pypi.org/pypi/growlnotify

|

.. image:: https://api.codacy.com/project/badge/Grade/b3ea7786516b42dfbb667cbe4fbf6d52
	:target: https://www.codacy.com/app/russianidiot/growlnotify-py

.. image:: https://codeclimate.com/github/russianidiot/growlnotify.py/badges/gpa.svg
	:target: https://codeclimate.com/github/russianidiot/growlnotify.py

.. image:: https://landscape.io/github/russianidiot/growlnotify.py/master/landscape.svg?style=flat
	:target: https://landscape.io/github/russianidiot/growlnotify.py

.. image:: https://scrutinizer-ci.com/g/russianidiot/growlnotify.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/russianidiot/growlnotify.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install growlnotify`





Usage
`````


.. code:: python

	>>> from growlnotify import growlnotify
	
	>>> growlnotify(title,message,)



Examples
````````


.. code:: python

	>>> growlnotify("title")
	
	>>> growlnotify(u"unicode") # unicode
	
	>>> growlnotify("title",message="message") # message
	
	>>> growlnotify("title",sticky=True) # sticky
	
	import os
	>>> growlnotify("title",message="message",app="Finder",url="file://%s" % os.environ["HOME"])





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/growlnotify.py.svg
	:target: https://github.com/russianidiot/growlnotify.py/issues

