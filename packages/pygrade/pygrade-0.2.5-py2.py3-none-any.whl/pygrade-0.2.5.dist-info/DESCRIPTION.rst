===============================
pygrade
===============================

.. image:: https://img.shields.io/pypi/v/pygrade.svg
        :target: https://pypi.python.org/pypi/pygrade

.. image:: https://img.shields.io/travis/tapilab/pygrade.svg
        :target: https://travis-ci.org/tapilab/pygrade

.. image:: https://readthedocs.org/projects/pygrade/badge/?version=latest
        :target: https://readthedocs.org/projects/pygrade/?badge=latest
        :alt: Documentation Status


auto-grade python assignments

* Free software: ISC license
* Documentation: https://pygrade.readthedocs.org.

This library helps one create and grade programming assignments written in Python and submitted by students via Github.

Features include the ability to:

- Create private GitHub repositories for each student.
- Populate student repositories with starter code.
- Grade student assignments by running unittests against their code.
- Push grades and failing tests back to the student repositories.
- Summarize grades by test or student

See the example_ for a tutorial on usage.

.. _example: https://github.com/tapilab/pygrade/tree/master/example

Related libraries
-----------------

* teacherspet_ : manipulates github repos for teaching.

.. _teacherspet: https://github.com/education/teachers_pet

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage




History
-------
0.2.5 (2018-01-25)
---------------------
* Bugfixes
* New feature: delete student accounts

0.2.4 (2017-01-23)
---------------------
* Bugfixes
* Enforce alpha version of github3

0.2.3 (2016-10-14)
---------------------
* Bugfixes

0.2.2 (2016-10-14)
---------------------

* Support extra file for external deductions
* Summarize grades by student/test/etc.

0.1.8 (2016-01-16)
---------------------

* First fully functional version

0.1.0 (2016-01-01)
---------------------

* First release on PyPI.


