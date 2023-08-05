Jupyter docx bundler extension
==============================

|PyPi Version|

Jupyter bundler extension to export notebook as a docx file

Install
-------

Installing with pip
~~~~~~~~~~~~~~~~~~~

::

    pip install jupyter_docx_bundler
    jupyter bundlerextension enable --py jupyter_docx_bundler --sys-prefix

Installing with conda
~~~~~~~~~~~~~~~~~~~~~

::

    conda install -c mrossi jupyter_docx_bundler

Usage
-----

Adding Metadata
~~~~~~~~~~~~~~~

The bundle extension uses metadata of the notebook, if you you provide
it.

-  You can add a title by adding ``"title": "Notebook title"``
-  You can add authors by adding
   ``"authors": [{"name": "author1"}, {"name": "author2"}]``

The notebook metadata can be edited under *Edit* -> *Edit Notebook
Metadata*.

Hiding inputs or complete code cells
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can hide individual code cells or just their inputs by defining cell
tags:

-  ``nbconvert-remove-cell``: Remove the entire cell
-  ``nbconvert-remove-input``: Remove the input code of the cell

*(Currently there are no default values configured for these tags, the
ones listed above are defined in my code and not in
`nbconvert <https://github.com/jupyter/nbconvert>`__. This may will
change in the future.)*

Cell tags can be shown by activating the cell toolbar under *View* ->
*Cell Toolbar* -> *Tags*.

.. |PyPi Version| image:: https://img.shields.io/pypi/v/jupyter_docx_bundler.svg
   :target: https://pypi.python.org/pypi/jupyter_docx_bundler
