Indic transliteration tools
===========================

| |Build Status|
| |Documentation Status|

For users
=========

-  `Docs <http://indic-transliteration.readthedocs.io/en/latest/>`__.
-  For detailed examples and help, please see individual module files in
   this package.

Installation or upgrade:
------------------------

-  ``sudo pip install indic_transliteration -U``
-  ``sudo pip install git+https://github.com/sanskrit-coders/indic_transliteration/@master -U``
-  `Web <https://pypi.python.org/pypi/indic-transliteration>`__.

For contributors
================

Contact
-------

Have a problem or question? Please head to
`github <https://github.com/sanskrit-coders/indic_transliteration>`__.

Packaging
---------

-  ~/.pypirc should have your pypi login credentials.

   ::

       python setup.py bdist_wheel
       twine upload dist/* --skip-existing

.. |Build Status| image:: https://travis-ci.org/sanskrit-coders/indic_transliteration.svg?branch=master
   :target: https://travis-ci.org/sanskrit-coders/indic_transliteration
.. |Documentation Status| image:: https://readthedocs.org/projects/indic-transliteration/badge/?version=latest
   :target: http://indic-transliteration.readthedocs.io/en/latest/?badge=latest


