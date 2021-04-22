============
Contributing
============

Thank you for contributing!
We have tried to organize the site such that we can include a variety of content.

Overview
========

#. You can suggest comprehensive changes to the website using `GitHub <https://github.com/JakeGWater/vpifg.com>`_.

   #. Check out the official `Contributing Explainer <https://github.com/JakeGWater/vpifg.com/blob/main/README.md#contribute>`_

#. If you have never used GitHub, don't worry. There's a little bit of setup, but you can do everything from the website.
#. Try to follow the `Contributing Guidelines`_ as much as possible.
#. Once approved, your content will be merged and immediately visible.

Contributing Guidelines
=======================

We want the site to be helpful, comprehensive, and easy to navigate.
As such, there are a few guidelines we would like contributions to follow:

#. The :doc:`/CodeOfConduct` applies to all submissions.
#. Contributions **must** be centred around virtual production.
#. Your contribution must fit into one of the existing categories:

   #. `Workflow <#adding-workflows>`_
   #. `Guides <#adding-guides>`_
   #. :doc:`/studios`
   #. `Help <#adding-help>`_

Adding Workflows
----------------

#. Workflows should reference a series of :doc:`/guides` to be placed in `sources/guides <https://github.com/JakeGWater/vpifg.com/tree/main/source/guides>`_.
#. Incomplete workflows **must** be marked as `Work in Progress`_.
#. Workflows **must** include a :ref:`production-checklist` banner. See :doc:`/workflows/BURN`.
   Insert after your title::

        .. prodcheck::
            :4k: yes|no
            :timecode: yes|no
            :raw: yes|no
            :aces: yes|no
            :ndisplay: yes|no
            :live: yes|no
            :multicam: yes|no

   Choose ``yes`` or ``no`` for each option. 
   This produces something like:

   .. prodcheck::
        :4k: yes
        :timecode: yes
        :raw: no
        :aces: no
        :ndisplay: yes
        :live: yes
        :multicam: no

   **Important** your workflow does not need to check all boxes.

Adding Guides
-------------

#. Guides must be part of a workflow. If you have a general tip, consider adding a Help page instead.
#. Contribution which are not complete must be marked as `Work in Progress`_.
#. Please follow the `Referencing Content`_ and `Embedding Content`_ guidelines.
#. Images must be hosted from vpifg.com, add them to ``sources/_static/guides``.
   You **must** own the images, or be allowed to license the images for use on vpifg.com.

Adding Help
-----------

Sometimes content doesn't fit into a guide, but it is helpful nonetheless.
The guidelines for what goes and help our a little looser than what goes into a workflow or a guide.
Nonetheless, we want things to be centered around a virtual production.

Each Help article should be its own document in ``sources/help``.

Referencing Content
----------------------

#. External links **must** be `Citation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#citations>`_. 

   1. Refer to to the citation from your guide or workflow as follows::

       Use the [unrealengine]_ to ...
   2. Put the citation in :doc:`/references` as::

       .. [unrealengine] The unreal game engine `<https://www.unrealengine.com>`_

#. *Exceptions* 
    
   #. Studio pages (:doc:`/studios`) may use external links, including affiliate links.
   #. About pages may use external links.

Using citations keeps things under control, and ensures that all links are reusable and relevant.


Embedding Content
--------------------

Embedding content, such as videos, figures, slides is encouraged and permitted. 
The content must be served from one of the following domains:

- youtube.com
- docs.google.com
- figma.com

If you would like to add another domain, please `open an issue <https://github.com/JakeGWater/vpifg.com/issues/new>`_ to discuss.

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

