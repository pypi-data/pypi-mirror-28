Configuration guide
======================

The configuration guide provides a basic overview of the general
options and settings layout for the supported workflow managers.
Please refer to the workflow documentation pages for more specifice
instructions regarding a particular workflow.

Currently, the supported workflow managers are:

- `snakemake`_: a workflow management system written in python
- `nextflow`_: a fluent DSL for data-driven computational pipelines

Snakemake
----------

Snakemake can be configured through a configuration file that is
passed either via the ``--configfile`` command line option, or the
Snakefile ``configfile:`` directive. Once loaded, the configuration
settings can be accessed through the global python object ``config``.

Internally, configuration objects are `python dictionaries`_, where
the keys correspond to configuration options. This has the unfortunate
consequence that it is difficult to provide a documentation API to the
options. This text tries to address this issue, albeit in an
unsufficient manner. As a last resort, for now at least, one simply
has to look at the source code to get an idea of what the options do.
In most cases though, the key names themselves should give an idea of
what behaviour they target.

It is important to keep in mind that no validation of user-supplied
configuration files is done. Consequently, should the user supply a
non-defined configuration key, it will passed unnoticed by Snakemake.
This can be frustrating when debugging; you are sure that you have
changed a configuration value, only to notice later that the
configuration key was misspelled.

Implementation
^^^^^^^^^^^^^^^^

The configuration is constructed as a hierarchy of at most three
levels:[#]_

.. code-block:: yaml

   section:
     subsection:
       option:


The ``section`` level corresponds to an application, or a configuration
group of more general nature. The ``subsection`` can either be a new
configuration grouping, or an option to be set. For applications, the
``subsection`` often corresponds to a given rule. Finally, at the
``option`` level, an option is set.


Configuration sections
^^^^^^^^^^^^^^^^^^^^^^

For each workflow, there is a subdirectory named ``rules``. The
directory contains rules organized by directories and ``settings`` files
that provide default configuration values. Every rule directory has
its own settings file. There are two top-level settings file located
directly in the ``rules`` directory, namely ``main.settings`` and
``ngs.settings``.

settings
~~~~~~~~~

The ``settings`` section defines configurations of a general nature. 

.. code-block:: yaml

   settings:
     sampleinfo: sampleinfo.csv
     email: # email
     java:
	java_mem: 8g
	java_tmpdir: /tmp
     runfmt: "{SM}/{SM}_{PU}"
     samplefmt: "{SM}/{SM}"
     threads: 8
     temporary_rules:
       - picard_merge_sam
	
For all settings, see ``rules/main.settings``.

Importantly, many of these settings are *inherited* by the application
rules, so that changing ``threads`` to 4 in ``settings``, will set the
number of threads for all configurations that inherit this option.
However, you can fine-tune the behaviour of the inheriting rules to
override the value in ``settings``; see :ref:`application-settings`.

Here, the most important option is ``sampleinfo``, which **must** be
set. The ``runfmt`` and ``samplefmt`` options describe how the data is
organized. They represent `python miniformat strings`_, where the
entries correspond to columns in the sampleinfo file; hence, in this
case, the column **SM** and **PU** must be present in the sampleinfo
file. So, given the following sampleinfo file

.. code-block:: text

   SM,PU,DT,fastq
   s1,AAABBB11XX,010101,s1_AAABBB11XX_010101_1.fastq.gz
   s1,AAABBB11XX,010101,s1_AAABBB11XX_010101_2.fastq.gz
   s1,AAABBB22XX,020202,s1_AAABBB22XX_020202_1.fastq.gz
   s1,AAABBB22XX,020202,s1_AAABBB22XX_020202_2.fastq.gz

samplefmt will be formatted as ``s1/s1`` and runfmt as
``s1/s1_AAABBB11XX`` or ``s1/s1_AAABBB22XX``, depending on the run. The
formatted strings are used in the workflows as *prefixes* to identify
targets. Rules that operate on the runfmt will be prefixed by
``s1/s1_AAABBB11XX`` or ``s1/s1_AAABBB22XX``, rules that operate on the
sample level (i.e. after merging) will be prefixed by ``s1/s1``.

Currently, the tests define three different sample organizations.

.. code-block:: yaml

   sample:
     runfmt: "{SM}/{SM}_{PU}_{DT}"
     samplefmt: "{SM}/{SM}"
   sample_run:
     runfmt: "{SM}/{PU}_{DT}/{SM}_{PU}_{DT"}
     samplefmt: "{SM}/{SM}"
   sample_project_run:
     runfmt: "{SM}/{PID}/{PU}_{DT}/{PID}_{PU}_{DT"}
     samplefmt: "{SM}/{SM}"

However, it is trivial to add more configurations, should that be
deemed necessary.

ngs.settings
~~~~~~~~~~~~~

.. warning::

   The ngs.settings section is slightly disorganized.

``ngs.settings`` affect settings related to ngs analyses:

.. code-block:: yaml
   
   ngs.settings:
     annotation:
	   annot_label: ""
	   transcript_annot_gtf: ""
	   sources: []
     db:
	   dbsnp: ""
       ref: ref.fa
	   transcripts: []
	   build: ""
     fastq_suffix: ".fastq.gz"
     read1_label: "_1"
     read2_label: "_2"
     read1_suffix: ".fastq.gz"
     read2_suffix: ".fastq.gz"
     regions: []
     sequence_capture:
       bait_regions: []
	   target_regions: []


For all settings, see ``rules/ngs.settings``.

samples
~~~~~~~

The ``samples`` section is one of the few top-level configuration keys
that are actually set, in this case to a list of sample names.

.. _application-settings:

Application settings
~~~~~~~~~~~~~~~~~~~~~~~~~

Applications, i.e. bioinformatics software, are grouped in sections by
their application name. Subsections correspond to rules, or
subprograms. For instance, the entire bwa section looks as follows
(with a slight abuse of notation as we here mix yaml with python
objects):

.. code-block::  yaml
   
   bwa:
     cmd: bwa
     ref: config['ngs.settings']['db']['ref']
     index: ""
     index_ext: ['.amb', '.ann', '.bwt', '.pac', '.sa']
     threads: config['settings']['threads']
     mem:
       options:
  

Setting option ``threads`` would then override the value in ``settings``,
providing a means to fine-tune options on a per-application basis.

Workflow settings
~~~~~~~~~~~~~~~~~~~

Finally, the workflows comes with a configuration section called
``workflow``.


Nextflow
-----------

TODO.


.. _python dictionaries: https://docs.python.org/3.5/tutorial/datastructures.html#dictionaries
.. _python miniformat strings: https://docs.python.org/3/library/string.html#formatspec
.. _snakemake: https://snakemake.readthedocs.io/en/stable/
.. _nextflow: https://www.nextflow.io/

.. [#] Note that the configuration structure can vary depending on workflow since different developers work on different workflows. The structure described in this document was developed for the first iteration of the workflows.
