#######################################################
ScriptTester - utility for testing command line scripts
#######################################################

.. shared-text-body

**********
Quickstart
**********

Provides class to be instantiated in tests that check that scripts can be run
and give correct output.  Usually works something like this in a test module::

    import mymodule
    from scripttester import ScriptTester
    runner = ScriptTester(mymodule)

Then, in the tests, something like::

    code, stdout, stderr = runner.run_command(['my-script', my_arg])
    assert code == 0
    assert stdout == b'This script ran OK'

The class aims to find your scripts whether you have installed (with ``pip
install .`` or ``pip install -e .`` or ``python setup.py install``), or not.
If you have not installed, the scripts will not be on your system PATH, and we
have to find them.  The heuristic is to look (by default) in the directory
containing ``mymodule``; if there is a ``setup.py`` file there, and a
``scripts`` sub-directory, assume that directory contains the scripts.

Note there is no way of using this not-installed mechanism to find entrypoint
scripts, that have not been installed. To find these, we would have to run the
``setup.py`` file.

************
Installation
************

::

    pip install scripttester

****
Code
****

See https://github.com/matthew-brett/scripttester

Released under the BSD two-clause license - see the file ``LICENSE`` in the
source distribution.

`travis-ci <https://travis-ci.org/matthew-brett/scripttester>`_ kindly tests
the code automatically under Python versions 2.7, and 3.3 through 3.6.

The latest released version is at https://pypi.python.org/pypi/scripttester

*****
Tests
*****

* Install ``scripttester``
* Install the pytest_ testing framework::

    pip install pytest

* Run the tests with::

    py.test --pyargs scripttester

*******
Support
*******

Please put up issues on the `scripttester issue tracker`_.

.. standalone-references

.. |scripttester-documentation| replace:: `scripttester documentation`_
.. _scripttester documentation:
    https://matthew-brett.github.com/scripttester/scripttester.html
.. _documentation: https://matthew-brett.github.com/scripttester
.. _pandoc: http://pandoc.org
.. _jupyter: jupyter.org
.. _homebrew: brew.sh
.. _sphinx: http://sphinx-doc.org
.. _rest: http://docutils.sourceforge.net/rst.html
.. _scripttester issue tracker: https://github.com/matthew-brett/scripttester/issues
.. _pytest: https://pytest.readthedocs.io
.. _mock: https://github.com/testing-cabal/mock
