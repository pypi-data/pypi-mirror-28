======================
Sphinx Nameko MW Theme
======================

Official Ssphinx theme for Mediaware

Forked from Sphinx theme for `Nameko <https://github.com/onefinestay/nameko>`_.
and combined with elements from the `Better <https://github.com/irskep/sphinx-better-theme>`_
theme.

Sphinx Nameko theme was forked from `Sphinx Readable Theme <https://github.com/ignacysokolowski/sphinx-readable-theme>`_
and combined with elements of the `Read The Docs <https://github.com/snide/sphinx_rtd_theme>`_ theme.


Installation and setup
======================


Install from PyPI::

    $ pip install sphinx-nameko-mw-theme

And add this to your Sphinx ``conf.py``:

.. code-block:: python

    import sphinx_nameko_mw-theme

    html_theme_path = [sphinx_nameko_mw_theme.get_html_theme_path()]
    html_theme = 'nameko-mw'

Theme options
==============

Nameko MW theme has the following theme options available::

    html_theme_options = {

        # Show a logo in the document below the relative links
        # Path is to built file location, not source file location
        # Max width should be less than 940px
        'doc_logo': '_images/mylogo.png',

        # Include a link to the currently used theme in the footer
        'linktotheme': 'True'

}

Example
========

An example of Nameko MW theme can be seen at the `Github Pages site <https://penseleit.github.io/sphinx-nameko-mw-theme/>`_

License
=======

Sphinx Nameko-MW Theme is licensed under the MIT license.


Changelog
=========

Version 0.0.1
-------------

Initial fork

Version 0.0.4
-------------
- Added configuration options
- Modified layout.html template
- Modified nameko-mw.css_t file
