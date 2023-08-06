.. README.rst
.. Copyright (c) 2013-2018 Pablo Acosta-Serafini
.. See LICENSE for details


.. image:: https://badge.fury.io/py/ptrie.svg
    :target: https://pypi.python.org/pypi/ptrie
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/ptrie.svg
    :target: https://pypi.python.org/pypi/ptrie
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/ptrie.svg
    :target: https://pypi.python.org/pypi/ptrie
    :alt: Python versions supported

.. image:: https://img.shields.io/pypi/format/ptrie.svg
    :target: https://pypi.python.org/pypi/ptrie
    :alt: Format

|

.. image::
   https://travis-ci.org/pmacosta/ptrie.svg?branch=master

.. image::
   https://ci.appveyor.com/api/projects/status/
   7dpk342kxs8kcg5t/branch/master?svg=true
   :alt: Windows continuous integration

.. image::
   https://codecov.io/github/pmacosta/ptrie/coverage.svg?branch=master
   :target: https://codecov.io/github/pmacosta/ptrie?branch=master
   :alt: Continuous integration coverage

.. image::
   https://readthedocs.org/projects/pip/badge/?version=stable
   :target: http://pip.readthedocs.org/en/stable/?badge=stable
   :alt: Documentation status

|

Description
===========

.. role:: bash(code)
	:language: bash

.. [[[cog
.. import os, sys
.. from docs.support.term_echo import ste
.. file_name = sys.modules['docs.support.term_echo'].__file__
.. mdir = os.path.realpath(
..     os.path.dirname(os.path.dirname(os.path.dirname(file_name)))
.. )
.. import docs.support.requirements_to_rst
.. docs.support.requirements_to_rst.def_links(cog)
.. ]]]
.. _Astroid: https://bitbucket.org/logilab/astroid
.. _Cog: http://nedbatchelder.com/code/cog
.. _Coverage: http://coverage.readthedocs.org/en/coverage-4.0a5
.. _Docutils: http://docutils.sourceforge.net/docs
.. _Pmisc: http://pmisc.readthedocs.org
.. _Pylint: http://www.pylint.org
.. _Py.test: http://pytest.org
.. _Pytest-coverage: https://pypi.python.org/pypi/pytest-cov
.. _Pytest-xdist: https://pypi.python.org/pypi/pytest-xdist
.. _Sphinx: http://sphinx-doc.org
.. _ReadTheDocs Sphinx theme: https://github.com/snide/sphinx_rtd_theme
.. _Inline Syntax Highlight Sphinx Extension:
   https://bitbucket.org/klorenz/sphinxcontrib-inlinesyntaxhighlight
.. _Tox: https://testrun.org/tox
.. _Virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs
.. [[[end]]]

This module can be used to build, handle, process and search
`tries <http://wikipedia.org/wiki/Trie>`_

Interpreter
===========

The package has been developed and tested with Python 2.7, 3.5 and 3.6 under
Linux (Debian, Ubuntu), Apple OS X and Microsoft Windows

Installing
==========

.. code-block:: bash

	$ pip install ptrie

Documentation
=============

Available at `Read the Docs <https://ptrie.readthedocs.org>`_

Contributing
============

1. Abide by the adopted `code of conduct
   <http://contributor-covenant.org/version/1/3/0>`_

2. Fork the `repository <https://github.com/pmacosta/ptrie>`_ from
   GitHub and then clone personal copy [#f1]_:

	.. code-block:: bash

		$ git clone \
		      https://github.com/[github-user-name]/ptrie.git
                Cloning into 'ptrie'...
                ...
		$ cd ptrie
		$ export PTRIE_DIR=${PWD}

3. Install the project's Git hooks and build the documentation. The pre-commit
   hook does some minor consistency checks, namely trailing whitespace and
   `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ compliance via
   Pylint. Assuming the directory to which the repository was cloned is
   in the :bash:`$PTRIE_DIR` shell environment variable:

	.. code-block:: bash

		$ ${PTRIE_DIR}/sbin/complete-cloning.sh
                Installing Git hooks
                Building ptrie package documentation
                ...

4. Ensure that the Python interpreter can find the package modules
   (update the :bash:`$PYTHONPATH` environment variable, or use
   `sys.paths() <https://docs.python.org/2/library/sys.html#sys.path>`_,
   etc.)

	.. code-block:: bash

		$ export PYTHONPATH=${PYTHONPATH}:${PTRIE_DIR}

5. Install the dependencies (if needed, done automatically by pip):

    .. [[[cog
    .. import docs.support.requirements_to_rst
    .. docs.support.requirements_to_rst.proc_requirements(cog)
    .. ]]]


    * `Astroid`_ (1.6.0 or newer)

    * `Cog`_ (2.5.1 or newer)

    * `Coverage`_ (4.4.2 or newer)

    * `Docutils`_ (0.14 or newer)

    * `Inline Syntax Highlight Sphinx Extension`_ (0.2 or newer)

    * `Pmisc`_ (1.3.1 or newer)

    * `Py.test`_ (3.3.2 or newer)

    * `Pylint`_ (1.8.1 or newer)

    * `Pytest-coverage`_ (2.5.1 or newer)

    * `Pytest-xdist`_ (optional, 1.22.0 or newer)

    * `ReadTheDocs Sphinx theme`_ (0.1.9 or newer)

    * `Sphinx`_ (1.6.6 or newer)

    * `Tox`_ (2.9.1 or newer)

    * `Virtualenv`_ (15.1.0 or newer)

    .. [[[end]]]

6. Implement a new feature or fix a bug

7. Write a unit test which shows that the contributed code works as expected.
   Run the package tests to ensure that the bug fix or new feature does not
   have adverse side effects. If possible achieve 100% code and branch
   coverage of the contribution. Thorough package validation
   can be done via Tox and Py.test:

	.. code-block:: bash

            $ tox
            GLOB sdist-make: .../ptrie/setup.py
            py26-pkg inst-nodeps: .../ptrie/.tox/dist/ptrie-...zip

   `Setuptools <https://bitbucket.org/pypa/setuptools>`_ can also be used
   (Tox is configured as its virtual environment manager):

	.. code-block:: bash

	    $ python setup.py tests
            running tests
            running egg_info
            writing requirements to ptrie.egg-info/requires.txt
            writing ptrie.egg-info/PKG-INFO
            ...

   Tox (or Setuptools via Tox) runs with the following default environments:
   ``py27-pkg``, ``py35-pkg`` and ``py36-pkg`` [#f2]_. These use the 2.7, 3.5
   and 3.6 interpreters, respectively, to test all code in the documentation
   (both in Sphinx ``*.rst`` source files and in docstrings), run all unit
   tests, measure test coverage and re-build the exceptions documentation. To
   pass arguments to Py.test (the test runner) use a double dash (``--``) after
   all the Tox arguments, for example:

	.. code-block:: bash

	    $ tox -e py27-pkg -- -n 4
            GLOB sdist-make: .../ptrie/setup.py
            py27-pkg inst-nodeps: .../ptrie/.tox/dist/ptrie-...zip
            ...

   Or use the :code:`-a` Setuptools optional argument followed by a quoted
   string with the arguments for Py.test. For example:

	.. code-block:: bash

	    $ python setup.py tests -a "-e py27-pkg -- -n 4"
            running tests
            ...

   There are other convenience environments defined for Tox [#f3]_:

    * ``py27-repl``, ``py35-repl`` and ``py36-repl`` run the 2.7, 3.6 or 3.6
      REPL, respectively, in the appropriate virtual environment. The ``ptrie``
      package is pip-installed by Tox when the environments are created.
      Arguments to the interpreter can be passed in the command line after a
      double dash (``--``)

    * ``py27-test``, ``py35-test`` and ``py36-test`` run py.test using the
      Python 2.7, 3.5 or Python 3.6 interpreter, respectively, in the
      appropriate virtual environment. Arguments to py.test can be passed in the
      command line after a double dash (``--``) , for example:

	.. code-block:: bash

	    $ tox -e py36-test -- -x test_ptrie.py
            GLOB sdist-make: [...]/ptrie/setup.py
            py36-test inst-nodeps: [...]/ptrie/.tox/dist/ptrie-1.1rc1.zip
            py36-test installed: -f file:[...]
            py36-test runtests: PYTHONHASHSEED='1264622266'
            py36-test runtests: commands[0] | [...]py.test -x test_ptrie.py
            ===================== test session starts =====================
            platform linux -- Python 3.6.4, pytest-3.3.1, py-1.5.2, pluggy-0.6.0
            rootdir: [...]/ptrie/.tox/py36/share/ptrie/tests, inifile: pytest.ini
            plugins: xdist-1.21.0, forked-0.2, cov-2.5.1
            collected 414 items
            ...

    * ``py27-cov``, ``py35-cov`` and ``py36-cov`` test code and branch coverage
      using the 2.7, 3.5 or 3.6 interpreter, respectively, in the appropriate
      virtual environment. Arguments to py.test can be passed in the command
      line after a double dash (``--``). The report can be found in
      :bash:`${ptrie_DIR}/.tox/py[PV]/usr/share/ptrie/tests/htmlcov/index.html`
      where ``[PV]`` stands for ``27``, ``35`` or ``36`` depending on the
      interpreter used

8. Verify that continuous integration tests pass. The package has continuous
   integration configured for Linux (via `Travis <http://www.travis-ci.org>`_)
   and for Microsoft Windows (via `Appveyor <http://www.appveyor.com>`_).
   Aggregation/cloud code coverage is configured via
   `Codecov <https://codecov.io>`_. It is assumed that the Codecov repository
   upload token in the Travis build is stored in the :bash:`${CODECOV_TOKEN}`
   environment variable (securely defined in the Travis repository settings
   page).

9. Document the new feature or bug fix (if needed). The script
   :bash:`${PTRIE_DIR}/sbin/build_docs.py` re-builds the whole package
   documentation (re-generates images, cogs source files, etc.):

	.. [[[cog ste('build_docs.py -h', 0, mdir, cog.out) ]]]

	.. code-block:: bash

	    $ ${PMISC_DIR}/sbin/build_docs.py -h
	    usage: build_docs.py [-h] [-d DIRECTORY] [-r]
	                         [-n NUM_CPUS] [-t]

	    Build ptrie package documentation

	    optional arguments:
	      -h, --help            show this help message and exit
	      -d DIRECTORY, --directory DIRECTORY
	                            specify source file directory
	                            (default ../ptrie)
	      -r, --rebuild         rebuild exceptions documentation.
	                            If no module name is given all
	                            modules with auto-generated
	                            exceptions documentation are
	                            rebuilt
	      -n NUM_CPUS, --num-cpus NUM_CPUS
	                            number of CPUs to use (default: 1)
	      -t, --test            diff original and rebuilt file(s)
	                            (exit code 0 indicates file(s) are
	                            identical, exit code 1 indicates
	                            file(s) are different)


	.. [[[end]]]

    Output of shell commands can be automatically included in reStructuredText
    source files with the help of Cog_ and the :code:`docs.support.term_echo` module.



    Similarly Python files can be included in docstrings with the help of Cog_
    and the :code:`docs.support.incfile` module


.. rubric:: Footnotes

.. [#f1] All examples are for the `bash <https://www.gnu.org/software/bash/>`_
   shell

.. [#f2] It is assumed that all the Python interpreters are in the executables
   path. Source code for the interpreters can be downloaded from Python's main
   `site <http://www.python.org/downloads>`_

.. [#f3] Tox configuration largely inspired by
   `Ionel's codelog <http://blog.ionelmc.ro/2015/04/14/
   tox-tricks-and-patterns/>`_


License
=======

The MIT License (MIT)

Copyright (c) 2013-2018 Pablo Acosta-Serafini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
.. CHANGELOG.rst
.. Copyright (c) 2013-2018 Pablo Acosta-Serafini
.. See LICENSE for details

Changelog
=========

* 1.1.0 [2018-01-18]: Dropped support for Python interpreter versions 2.6, 3.3
  and 3.4. Updated dependencies versions to their current versions

* 1.0.6 [2017-02-09]: Package build enhancements and fixes

* 1.0.5 [2017-02-07]: Python 3.6 support

* 1.0.4 [2016-06-11]: Minor documentation build bug fix

* 1.0.3 [2016-05-13]: Documentation update

* 1.0.2 [2016-05-11]: Documentation update

* 1.0.1 [2016-05-02]: Minor documentation and testing enhancements

* 1.0.0 [2016-04-25]: Final release of 1.0.0 branch

* 1.0.0rc1 [2016-04-25]: Initial commit, forked off putil PyPI package


