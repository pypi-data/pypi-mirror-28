Introduction
============

The name **candlestick** comes from the early times when the telephone has been invented.
One of the first model of a telephone was a stick which has been placed on table where the speaker
had to talk into.

.. image:: docs/candlestick.jpg

This module provides a javascript library for automatically generate phone links.
A treeWalker walks through the whole DOM and collects all :code:`textNodes`. If a node
matches a phone number the number will be replaced with a :code:`<a href="tel:phonenumber">Your phonenumber</a>`
link. Existing links or inputfields are not affected.

By default the `candlestick.integration.js` is being loaded which converts all phone numbers in the `body` initially.

.. contents:: Table of Contents

Compatibility
-------------

Plone 4.3.x


Installation
============

- Add the package to your buildout configuration:

.. code:: ini

    [instance]
    eggs +=
        ...
        ftw.candlestick


Development
===========

**Python:**

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buidlout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.candlestick
- Issues: https://github.com/4teamwork/ftw.candlestick/issues
- Pypi: http://pypi.python.org/pypi/ftw.candlestick
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.candlestick


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.candlestick`` is licensed under GNU General Public License, version 2.

Client library
==============

Getting Started
---------------

The client library depends on `Grunt <http://gruntjs.com/>`_. Assuming
you already have **Node.js** installed on your system, run the following command:

.. code:: bash

  sudo npm install -g grunt

To install the dependencies, run the following command:

.. code:: bash

  npm install

And with **npm** you get the following packages:

- `Grunt <http://gruntjs.com/>`_ - JavaScript task runner.
- `Babel <https://babeljs.io/>`_ - ES6 Transpiler.
- `Browserify <http://browserify.org/>`_ - Dependency Bundler
- `Karma <http://karma-runner.github.io/>`_ - JavaScript test runner.
- `Jasmine <http://jasmine.github.io/>`_ - JavaScript test suite.
- `Chai <http://chaijs.com/>`_ - JavaScript Assertion Library.

Usage
-----

Run the following command to re-build the library:

.. code:: bash

  grunt build

Run the following command to watch for changes which trigger a rebuild:

.. code:: bash

  grunt

Build options
-------------

See https://github.com/substack/browserify-handbook for more information about browserify.

Source Maps
-----------

Browserify comes with a built-in support to generate source maps. It is already enabled by default, but feel free to disable source maps. Refer to `this article <https://developers.google.com/chrome-developer-tools/docs/javascript-debugging#source-maps>`_
to enable source maps in Google Chrome, if you haven't already done so.

Tests
-----

Run all tests

.. code:: bash

  grunt test

Run a specific test

.. code:: bash

  grunt test --grep="Name of your test"

Initialization
--------------

Converts all phone numbers to links

.. code:: javascript

  window.candlestick();

