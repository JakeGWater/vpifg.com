sphinxcontrib-images
====================

sphinxcontrib-images (formerly `sphinxcontrib-fancybox
<https://pypi.python.org/pypi/sphinxcontrib-fancybox>`_).

Easy thumbnails in Sphinx documentation (focused on HTML).

* `Documentation <https://sphinxcontrib-images.readthedocs.io>`_
* `Repository (GitHub) <https://github.com/sphinx-contrib/images/>`_
* `PyPI <https://pypi.python.org/pypi/sphinxcontrib-images/>`_
* `TravisCI <https://travis-ci.com/sphinx-contrib/images>`_

  .. image:: https://api.travis-ci.com/sphinx-contrib/images.svg?branch=master
      :target: https://travis-ci.com/sphinx-contrib/images 

Features
--------

* Show thumbnails instead of full size images inside documentation (HTML).
* Ability to zoom/enlarge picture using LightBox2 (HTML).
* Ability to group pictures
* Download remote pictures and keep it in cache (if requested)
* Support for other formats (latex, epub, ... - fallback to image directive)
* Easy to extend (add own backend in only few lines of code)

  * Add other HTML "preview" solution than LightBox2
  * Add better support to non-HTML outputs
  * Preprocess images

TODO
^^^^

* Make proper thumbnails (scale down images)

How to install?
---------------

Instalation through pip: ::

    pip install sphinxcontrib-images

or through the GitHub: ::

    pip install git+https://github.com/sphinx-contrib/images

Next, you have to add extension to ``conf.py`` in your Sphinx project. ::

    extensions = [
              …
              'sphinxcontrib.images',
              …
              ]


How to use it?
--------------

Example: ::

    .. thumbnail:: picture.png


You can also override the default ``image`` directive provided by Sphinx.
Check the documentation for all configuration options.


Questions and suggestions
-------------------------

If you have any suggstions, patches, problems - please use
`GitHub Issues <https://github.com/sphinx-contrib/images/issues>`_.
