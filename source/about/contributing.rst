============
Contributing
============

Thank you for contributing!
We have tried to organize the site such that we can include a variety of content.

Overview
--------

#. Open a pull-request on GitHub with any content, even an empty file. This gives us a place to begin the conversation.
#. Work with the maintainers to craft your content for the site.
#. Try to follow the `Guidelines`_ as much as possible.
#. Once approved, your content will be merged and immediately visible.

Guidelines
----------

Contributions whenever possible should adhere to the following guidelines:

#. Contributions must be centred around virtual production.
#. Contributions should try to fit into the existing pattern. As a workflow, reference, studio setup, or resource.
#. Contributions must be :term:`Production Ready` or clearly marked as `Experimental`_.
#. Contribution which are not complete must be marked as `Work in Progress`_.
#. External Links:

   #. Must go in the relevant :doc:`/references` section. Use a `Citation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#citations>`_ to cross-link from elsewhere.
   #. *Exception* studio pages (:doc:`/studios`) may use external links, including affiliate links.

#. Embedding content, such as videos, figures, slides is encouraged and permitted. The content origin must be on our list of `Allowed Embedding Domains`_.
#. Images must be hosted from vpifg.com
#. Use `References for External Content`_

Allowed Embedding Domains
--------------------------

- youtube.com
- docs.google.com
- figma.com

Work in Progress
----------------

Any incomplete content must be marked as a work in progress with the following display:

.. wip::

Insert the following code immediately after the page title.

.. code-block:: rst

    .. wip::

If content is also experimental, it should be marked as both.

Experimental
------------

We encourage experimental setups, but we don't want to send people down the wrong path.
Experimental pages should begin with the following display:

.. experimental::

Insert the following code into the beginning of your page:

.. code-block:: rst

    .. experimental::

References for External Content
-------------------------------

All references to external content should use `citations <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#citations>`_ whenever possible.

For example:

1. Refer to to the citation from your guide or workflow as follows::

    Use the [unrealengine]_ to ...

2. Cite the content under the relevant :doc:`/references` file as::

    .. [unrealengine] The unreal game engine `<https://www.unrealengine.com>`_

Using citations keeps things under control, and ensures that all links are reusable and relevant.
