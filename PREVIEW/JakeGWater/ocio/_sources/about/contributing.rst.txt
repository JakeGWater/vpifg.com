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
#. Try to follow the `Contributing Guidelines`_ as much as possible,
   but it's okay to skim this section for now.
#. Once approved, your content will be merged and immediately visible.

Contributing Guidelines
=======================

We want the site to be helpful, comprehensive, and easy to navigate.
As such, there are a few guidelines we would like contributions to follow:

#. The :doc:`/CodeOfConduct` applies to all submissions.
#. Contributions **must** be centred around virtual production.
#. Your contribution must fit into one of the existing categories:

   #. `Adding Workflows <#adding-workflows>`_
   #. `Adding Guides <#adding-guides>`_
   #. `Adding Studios <#adding-studios>`_
   #. `Adding Help <#adding-help>`_

Adding Workflows
----------------

#. Workflows should reference a series of :goto:`guides` to be placed in `sources/guides <https://github.com/JakeGWater/vpifg.com/tree/main/source/guides>`_.
#. Workflows **must** include a Production Checklist banner. See :goto:`workflows/BURN`.
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

.. _adding-guides:

Adding Guides
-------------

If workflows are recipes, then guides are ingredients.
While workflows can be *seasoned to taste* a guide is more all-or-nothing.

Try to keep the following in mind:

#. Guides must be part of a workflow. 
   If you have a general tip, consider adding a Help page instead.
#. A guide must be complete before it will be published.
#. Please follow the `Referencing Content`_, `Adding Media`_, and `Embedding Content`_ guidelines.
#. Guides should link to pre-requisites, next steps, or alternative approaches.
   Keep your guide sizes reasonable.

Guide Template
^^^^^^^^^^^^^^

You can copy-paste the following into your new guide

.. code-block:: rst

   :author: YOUR NAME
   :author_url: YOUR LINK
   :date: THE DATE

   ================
   YOUR GUIDE TITLE
   ================

   .. deps:deps::

   .. deps:lesson::

      IN TWO SENTENCES DESCRIBE THIS GUIDES OBJECTIVE
   
   ANY PARAGRAPH, SECTION, ETC CONTENT

For any pre-requisites add

.. code-block:: rst

   .. deps:dep:: DEP TITLE

      DESCRIBE THE DEP :goto:`guides/GUIDE-NAME`.

If the guide does not exist, add a *placeholder* file at `source/guides/GUIDE-NAME.rst`

.. code-block:: rst

   ================
   GUIDE NAME TITLE
   ================

   .. milestone::

This will automatically track the guide in our backlog. For next steps, use `.. deps:next:: NEXT TITLE` similar to above.

Adding Media
------------

#. Images must:
   
   #. be hosted from vpifg.com by adding them to the repository, or
   #. be hosted on one of:

      - https://postimages.org/
      - https://cubeupload.com/
   
#. Images hosted on external sites might be copied to vpifg at any time.
   You **must** own the copyright to the image, or be allowed to license it.

Adding Help
-----------

Sometimes content doesn't fit into a guide, but it is helpful nonetheless.
The guidelines for what goes and help our a little looser than what goes into a workflow or a guide.
Still, we prefer help articles that:

#. are centered around a virtual production
#. address a specific technical hurdle
#. are short and to the point
#. include diagrams, images, and videos

Each Help article should be its own document in ``sources/help``.

Referencing Content
----------------------

#. External links **must** be `Citations <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#citations>`_. 

   #. Refer to to the citation from your guide or workflow as follows::

       Use the [unrealengine]_ to ...
   #. Add the citation, either in the same document, or in :goto:`references` as::

       .. [unrealengine] The unreal game engine `<https://www.unrealengine.com>`_
   #. Keep in mind, your citation might be relocated to :goto:`references`.

#. *Exceptions* 
    
   #. Studio pages (:goto:`studios`) may use external links, including affiliate links.
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

.. _adding-studios:

Adding Studios
--------------

Feel free to add your studio to :doc:`/studios`.

#. All content must follow our :doc:`/CodeOfConduct`.
#. Limit to a single page in `source/studios <https://github.com/JakeGWater/vpifg.com/tree/main/source/studios>`_.
#. You are encouraged to:
   
   #. Link to your website.
   #. Advertise any virtual production services.
   #. List your equipment, and even include affiliate links. Be specific if you can, including model numbers.
   #. Describe your vision for virtual production.
   #. Include photos of your studio.

#. Fore everything above, it should be limited to virtual production.
#. There are no size minimums. A home setup is just as good as a large studio.
