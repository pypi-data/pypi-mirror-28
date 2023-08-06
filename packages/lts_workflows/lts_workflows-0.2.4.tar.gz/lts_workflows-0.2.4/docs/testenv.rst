The workflow test environment
==============================

The workflow test environment [#f1]_ is built using the `pytest`_
framework. All workflows have tests that test minimal features of a
workflow, such as listing rules or printing help messages. In
addition, by installing the pytest plugin `pytest_ngsfixtures`_, the
workflows can be tested on small data sets.


Running workflow tests
-----------------------

There are two different ways to run the tests, depending on
installation mode. If the _workflow was installed as a package, either
via ``python setup.py install`` or a ``conda`` install, running

.. code-block:: console

   $ pytest --pyargs workflow

will run the tests. In addition, if `pytest_ngsfixtures`_ is
installed, the workflow will be run on a small test data set.

:mod:`lts_workflows` provides a number of pytest options (see
:ref:`testenv-additional-options`). Unfortunately, they are not loaded
when running the tests as described above. Rather, the full path to
the test file must be given for the options to load:


.. code-block:: console
		
   $ pytest /path/to/workflow/tests/ -h


The test suite will first setup and install local conda environments
necessary for the tests, and then run the tests. Please note
that the intended use of the local conda environments is to run the
tests only, **not** to run analyses based on the workflows.

Alternatively, by applying the ``-D`` option the test conda enviroment
setup is disabled. This obviously requires that the dependencies are
already installed (see section Installing dependencies below).


.. _testenv-additional-options:

Additional options
---------------------------

:py:mod:`lts_workflows` provides a helper function
:py:meth:`lts_workflows.pytest.plugin.addoptions` for adding pytest
options. Depending on the workflow engine, different options are
added. As an example, running the following setup code

.. code-block:: python

   def pytest_addoption(parser):
       group = parser.getgroup("ltssm_scrnaseq", "single cell rna sequencing options")
       lts_pytest.addoption(group)
		
in a pytest `conftest`_ file will add the following options to the
test suite:

.. code-block:: console

   single cell rna sequencing options:
     --no-slow             don't run slow tests
     -H, --hide-workflow-output
			   hide workflow output
     -T THREADS, --threads=THREADS
			   number of threads to use
     -D, --disable-test-conda
			   disable test conda setup; instead use user-supplied
			   environments, where the activated environment hosts
			   snakemake
     --conda-install-dir=CONDA_INSTALL_DIR
			   set conda install dir
     --conda-update        update local conda installation
     -2 PYTHON2_CONDA, --python2-conda=PYTHON2_CONDA
			   name of python2 conda environment [default: py2.7]
     -C, --use-conda       pass --use-conda flag to snakemake workflows; will
			   install conda environments on a rule by rule basis


All tests that execute workflows have been marked as *slow*. To
disable these tests, add the ``--no-slow`` option. By default,
workflow output is sent to stdout which is captured. If you want to
follow progress, add the regular pytest ``-s`` option. The ``-T``
option states how many threads/processes snakemake will use and can be
set to increase the speed of the slow tests. Finally, the test
environment will check if there is a conda environment called
``py2.7`` and if so, add the bin path to ``PATH``. Use the ``-2``
option if your python2 conda environment is named differently.

Note that the workflow directories should contain conda environment
files ``environment.yaml`` and ``environment-27.yaml`` that define the
depencies for a workflow. You can apply the latter to you python2
repository by issuing

.. code-block:: console
		
   $ conda env update -n python2env -f environment-27.yaml

Local conda installs
-------------------------

By default, the test setup will automatically download and install all
required packages via conda to ``$HOME/.conda_env``. By passing the
option ``--disable-test-conda`` (or ``-D``), dependencies will not be
installed by default. The following sections describe the steps needed
to setup personal conda environments with the required packages.

Installing dependencies with deploy_workflow.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning:: Due to refactorization, this is currently broken; see
             `issue #1`_.

The helper script ``deploy_workflow.py`` can be employed to install
required workflow dependencies in user-specified conda environments.


Semi-automated installation of snakemake and dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Setup a conda python3 environment that hosts snakemake:

.. code-block:: console
		
   $ conda create -n py3.5 -c bioconda snakemake python=3.5


Some workflows have python2 program dependencies. Create a conda
environment for these packages too:

.. code-block:: console
		
   $ conda create -n py2.7  python=2.7

Every workflow has a conda environment file, ``environment.yaml`` and
possibly ``environment-27.yaml`` that list the necessary dependencies.
You can update your conda python environments like so:

.. code-block:: console
		
   $ conda env update -n=py3.5 -f /path/to/environment.yaml
   $ conda env update -n=py2.7 -f /path/to/environment-27.yaml

Semi-automated installation of snakemake and dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unfortunately, nextflow requires java sdk <=8.0, whereas gatk requires
java sdk >=8.0. For this reason, it is recommended to install nextflow
in a separate conda environment:

.. code-block:: console
		
   $ conda create -n py3.5 -c bioconda nextflow python=3.5

Test fixtures
--------------------

TODO.

Hints on developing workflows
-----------------------------------

Use the test run wrapper functions in
:py:mod:`lts_workflow.pytest.helpers` to setup tests. They will create
a file ``command.sh`` located in the test output directory that can be
rerun to aid in debugging.


Testing external data sources
-------------------------------

If you have data that you want to test, bot whose sample layout is not
yet provided by the fixtures, you have to run snakemake as usual:


.. code-block:: console
		
   $ snakemake -s /path/to/Snakefile -d /path/to/sample_data --configfile /path/to/config.yaml targetname

You then obviously need to create a config file and a sampleinfo file.
You can also use the factory functions in `pytest_ngsfixtures`_ to
generate custom fixtures that resemble your sample layout.


.. _pytest: http://docs.pytest.org/en/latest
.. _pytest_ngsfixtures: https://github.com/percyfal/pytest-ngsfixtures
.. _conftest: http://doc.pytest.org/en/latest/writing_plugins.html#local-conftest-plugins
.. _issue #1: https://bitbucket.org/scilifelab-lts/lts-workflows/issues/1/deploy_workflowpy-is-broken


.. [#f1] This section does **not** describe how to run the test suite
         for :mod:`lts-workflows`. Rather, it describes general
         features of running workflow tests. Obviously, a workflow has
         to be installed for this section to apply.
