Matplotlib documentation
========================


Building the documentation
--------------------------

To build the documentation, you will need additional dependencies:

* Sphinx-1.3 or later (version 1.5.0 is not supported)
* numpydoc 0.4 or later
* IPython
* mock
* colorspacious
* pillow
* graphviz

All of these dependencies *except graphviz* can be installed through pip::

  pip install -r ../doc-requirements.txt

or all of them via conda and pip::

  conda install sphinx numpydoc ipython mock graphviz pillow \
    sphinx-gallery
  pip install colorspacious

To build the HTML documentation, type ``python make.py html`` in this
directory. The top file of the results will be ./build/html/index.html

**Note that Sphinx uses the installed version of the package to build the
documentation**: Matplotlib must be installed *before* the docs can be
generated.

You can build the documentation with several options:

* `--small` saves figures in low resolution.
* `--allowsphinxwarnings`: Don't turn Sphinx warnings into errors.
* `-n N` enables parallel build of the documentation using N process.

Organization
-------------

This is the top level build directory for the Matplotlib
documentation.  All of the documentation is written using sphinx, a
python documentation system built on top of ReST.  This directory contains

* users - the user documentation, e.g., plotting tutorials, configuration
  tips, etc.

* devel - documentation for Matplotlib developers

* faq - frequently asked questions

* api - placeholders to automatically generate the api documentation

* mpl_toolkits - documentation of individual toolkits that ship with
  Matplotlib

* make.py - the build script to build the html or PDF docs

* index.rst - the top level include document for Matplotlib docs

* conf.py - the sphinx configuration

* _static - used by the sphinx build system

* _templates - used by the sphinx build system

* sphinxext - Sphinx extensions for the mpl docs

* mpl_examples - a link to the Matplotlib examples in case any
  documentation wants to literal include them
