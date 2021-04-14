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
#. Contribution should be complete. The reader should not have to leave the site to finish reading. For example, a workflow cannot be incomplete but point to an external site for the remaining steps.
    #. Links to external resources must be in the :doc:`/resources` section. Other content should cross-link to the relevant content in resources.
    #. Content that is a `Work in Progress`_ is allowed, but must be clearly marked as such. Works in progress may reference external sites in `Comments <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#comments>`_. Note that works in progress which do not move forward may be removed.
#. Embedding complex content, such as videos, figures, slides is encouraged and permitted. The content origin must be on our list of `Approved Domains`_.
#. Images must be hosted from vpifg.com

Approved Domains
----------------

- youtube.com
- docs.google.com
- figma.com

Work in Progress
----------------

Any incomplete content must be marked as a work in progress with the following display:

.. caution::

    This content is a **Work in Progress** and may be incomplete.

.. code-block:: rst

    .. caution::

        This content is a **Work in Progress** and may be incomplete.

If content is also experimental, it should be marked as both.

Experimental
------------

We encourage experimental setups, but we don't want to send people down the wrong path.
Experimental pages should begin with the following display:

.. danger::

    This content is marked as **Experimental**, and may not be :term:`Production Ready`.

Insert the following code into the beginning of your page:

.. code-block:: rst

    .. danger::

        This content is marked as **Experimental**, and may not be :term:`Production Ready`.

Referencing Resources
---------------------

All references to external resources should use `citations <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#citations>`_ whenever possible.

For example:

1. Refer to to the citation from your guide or workflow as follows::

    Use the [unrealengine] to ...
2. Cite the resource under the relevant :doc:`/resources` file as::

    .. [unrealengine] The unreal game engine `<https://www.unrealengine.com>`_

Using citations keeps things under control, and ensures that all links are reusable and relevant.
