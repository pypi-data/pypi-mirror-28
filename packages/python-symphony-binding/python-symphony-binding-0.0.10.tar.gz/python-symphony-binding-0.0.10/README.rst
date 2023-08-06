A Symphony Python Language Binding Module
=========================================

.. image:: https://img.shields.io/pypi/v/python-symphony-binding.svg
      :target: https://pypi.python.org/pypi/python-symphony-binding/

.. image:: https://img.shields.io/pypi/pyversions/python-symphony-binding.svg
      :target: https://pypi.python.org/pypi/python-symphony-binding/

.. image:: https://img.shields.io/pypi/format/python-symphony-binding.svg
      :target: https://pypi.python.org/pypi/python-symphony-binding/

.. image:: https://img.shields.io/badge/license-Apache%202-blue.svg
      :target: https://github.com/symphonyoss/python-symphony-binding/blob/master/LICENSE

.. image:: https://travis-ci.org/symphonyoss/python-symphony-binding.svg?branch=master
      :target: https://travis-ci.org/symphonyoss/python-symphony-binding

.. image:: https://www.versioneye.com/user/projects/584f26435d8a55003f2782a7/badge.svg?style=flat-square
      :target: https://www.versioneye.com/user/projects/584f26435d8a55003f2782a7



Requirements
------------

python-pip
openssl-dev
libgnutls-dev

Dependencies
------------

This project uses the following libraries:

* pip
* requests
* bravado


Contributing
------------

.. _hacking guide: HACKING.rst
Start by checking out the `hacking guide`_.

Next fork the repo, make your commits locally.
You can run CI / CD checks by doing:

First I recommend doing your work in a venv:

.. code:: text

    virtualenv symphony-test
    ./symphony-test/bin/activate

Then run tox

.. code:: text

    cd python-symphony-binding
    pip install --upgrade tox
    tox

Once you are happy with your code, open a pull request.
Try to limit pull requests to signle specific changes.
If you want to make a major change hit me up via symphony, 
I am Matt Joyce ( symphony corporate ).  I am glad to hear
ideas.  And I'd love to see this project take on a life of
it's own.
