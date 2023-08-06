Informatics Matters Pipelines Utilities
=======================================

The ``im-pipelines-utils`` module is a core set of utilities employed by
`Informatics Matters`_' computational pipelines, its automated *Pipeline
Tester* and distributed in a number of our container images.

pipelines_utils
---------------
A generally useful collection of utility modules for any Informatics Matters'
pipelines. These consist of utilities in the ``parameter_utils`` module
to process multi-value (comma-separated) command-line parameter values along
with numerous helper and convenience methods in ``utils`` for file
handling and logging.

``utils`` depends on the RDKit_ open source cheminformatics software,
which you will need to install separately if you need to use this module.

rdkit_utils
-----------
A package of utility modules providing convenient wrappers around the
corresponding ``rdkit`` distribution.

``rdkit_utils`` depends on the RDKit_ open source cheminformatics software,
which you will need to install separately if you need to use this module.

.. _RDKit: http://www.rdkit.org
.. _Informatics Matters: http://www.informaticsmatters.com


