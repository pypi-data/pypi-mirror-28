packageManifest
---------------

|pipeline| |coverage|

.. |pipeline| image:: https://gitlab.com/blueskyjunkie/package-manifest/badges/master/pipeline.svg
   :target: https://gitlab.com/blueskyjunkie/package-manifest/commits/master
   :alt: pipeline status

.. |coverage| image:: https://gitlab.com/blueskyjunkie/package-manifest/badges/master/coverage.svg
   :target: https://gitlab.com/blueskyjunkie/package-manifest/commits/master
   :alt: coverage report


|doi0.2.0|

.. |doi0.2.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1165137.svg
   :target: https://doi.org/10.5281/zenodo.1165137
   :alt: DOI v0.2.0


A Python 3 framework for creating and maintaining a generalised manifest of files inspired by the Python MANIFEST.in. The framework would typically used as the basis of some kind of packaging tool to define the file needed for distribution of the package.


.. contents::

.. section-numbering::

Main Features
=============

* YAML based file format
* Common manifest operations:

  * include/exclude
  * global include/exclude
  * recursive include/exclude
  * prune/graft

Installation
============

The simplest way to acquire ``packageManifest`` is using ``pip``.

.. code-block:: bash

   pip install packageManifest

Getting Started
===============

The manifest YAML file is simply a list of the include or exclude operations to comprise the formulation of files. There
are six different types of operations - the same as the Python MANIFEST.in_.

.. _MANIFEST.in: https://docs.python.org/2/distutils/sourcedist.html#manifest-template

Each include/exclude operation can take either a ``files`` directive or a ``directory`` directive, or both, depending
on the type of include/exclude being applied.

.. code-block:: yaml

   - include:
       files: [ 'LICENSE', 'README.md' ]
   - exclude:
       files: [ '*.orig' ]
   - recursive-include:
       directory:  'include'
       files: [ '*.h', '*.c' ]
   - recursive-exclude:
       directory: 'temp/subdir'
       files: [ '*' ]
   - global-include:
       files: [ 'Makefile' ]
   - global-exclude:
       files: [ '*.txt', '*.tmp', 'test' ]
   - prune:
       directory: 'bin'
   - graft:
       directory: 'src'

The ``files`` directive contains a list of unix-glob like patterns to be applied to files.
The ``directory`` directive contains a single character string of the directory.

Using the manifest file is simply a matter of importing the library and using the ``from_yamlFile`` class method to
import the operations and apply them to the specified root directory of the directory tree from which to extract files.

.. code-block:: python

   from package-manifest import Manifest

   thisManifest = Manifest.from_yamlFile( 'manifest.yml', '.' )

   manifestFiles = thisManifest.apply()

``manifestFiles`` now contains a Python set of the file names from the root directory ``'.'`` that have been filtered by
the operations specified in the file ``manifest.yml``.
