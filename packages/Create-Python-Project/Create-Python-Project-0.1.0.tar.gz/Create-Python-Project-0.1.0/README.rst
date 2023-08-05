.. image:: https://travis-ci.org/nmvalera/create-python-project.svg?branch=master
    :target: https://travis-ci.org/nmvalera/create-python-project#

.. image:: https://codecov.io/gh/nmvalera/create-python-project/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nmvalera/create-python-project

Create-Python-Project
=====================

This project is inspired from excellent `Create-React-App`_.
It implements a Command Line Interface to enable straightforward manipulation of Python projects.
It allows to easily create a new Python project from an existing Python project (named boilerplate) used as a template.
It does so by automically contextualizing a boilerplate to your project.

Multiple context information can be updated such as

- Project's name
- Author's information (name and email)
- Hyperlinks to specific resources (such as travisd badges)
- etc.

How does it work?
-----------------

When creating a new project Create-Python-Project

#. clones the boilerplate project
#. automatically applies modification to contextualize the boilerplate to your project
#. commit all modifications
#. manage remotes by setting origin to your new project url and setting an upstream to the boilerplate for later update

.. _Create-React-App: https://github.com/facebookincubator/create-react-app

Requirements
------------

Distribution
~~~~~~~~~~~~

It is highly recommended to use this project on Unix distribution.

Git
~~~

Having the latest version of ``git`` installed locally.

Python
~~~~~~

Create-Python-Project is compatible with Python 3.5 and 3.6.

Installation
------------

..  code-block:: sh

    $ pip install create-python-project

Creating a new project
----------------------

..  code-block:: sh

    $ create-python-project new -b https://github.com/nmvalera/boilerplate-python.git new-project
