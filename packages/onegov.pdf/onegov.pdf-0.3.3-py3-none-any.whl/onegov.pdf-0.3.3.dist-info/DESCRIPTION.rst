

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov PDF follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov PDF uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.pdf.png
  :target: https://travis-ci.org/OneGov/onegov.pdf
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.pdf/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.pdf?branch=master
  :alt: Project Coverage

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.pdf.svg
    :target: https://badge.fury.io/py/onegov.pdf
    :alt: Latest PyPI Release

License
-------
onegov.pdf is released under GPLv2

Changelog
---------
0.3.3 (2018-01-18)
~~~~~~~~~~~~~~~~~~~~~

- Fixes handling of whitespace in mini html.
  [msom]

0.3.2 (2018-01-11)
~~~~~~~~~~~~~~~~~~~~~

- Adds support for indentation of lists.
  [msom]

- Fixes handling of whitespace in mini html.
  [msom]

0.3.1 (2018-01-10)
~~~~~~~~~~~~~~~~~~~~~

- Requires Python 3.6.
  [href]

- Adds compatibility with onegov.file.
  [msom]

0.3.0 (2017-11-17)
~~~~~~~~~~~~~~~~~~~~~

- Rewrites the mini_html function to use list flowables and a HTML sanitizer/
  cleaner.
  [msom]

- Adds h4.
  [msom]

0.2.0 (2017-11-14)
~~~~~~~~~~~~~~~~~~~~~

- Adds a generic header and footer.
  [msom]

0.1.1 (2017-11-13)
~~~~~~~~~~~~~~~~~~~~~

- Adds lexwork PDF signer.
  [msom]

0.1.0 (2017-11-13)
~~~~~~~~~~~~~~~~~~~~~

- Initial Release


