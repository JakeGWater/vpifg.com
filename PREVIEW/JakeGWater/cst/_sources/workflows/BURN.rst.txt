#################
BURN Workflow
#################

.. prodcheck::
    :4k: yes
    :timecode: yes
    :raw: yes
    :aces: yes
    :ndisplay: no
    :live: no
    :multicam: no

Overview
==================

**Blackmagic, Unreal, Resolve, and Nuke.**

The BURN workflow is a green-screen, single camera, shot-oriented workflow for pre-recorded film or TV. 
It is designed to be small, cost-efficient, but able to achive high-quality output.
BURN is a compromise between mixed-reality and traditional green-screen workflows. BURN has two pieces:

1. All equipment records internally at its highest quality.
2. A lower-fidelity live-composite is captured, viewable, and recorded on-set during the shot.

The lower quality capture is immediately available for editing, and contains all the final vfx, but without any post-processing polish that may be applied.
After editing, the higher quality footage may be substituted in using timecode to insert any clips into their correct spot in the timeline.

.. rubric:: Illustsrated Workflow

.. raw:: html

    <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vTyVdwzfBvYXjmkwG5eYsrhs0YIabcefUiPRgfXbdiu_NToHf2SqT9aJ31ci7LT0pj-rlzt9Y-y5sHx/embed?start=false&loop=false&delayms=3000#slide=id.gcae64a3773_2_37" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>

Guides
======

Pre-Production
--------------

#. :goto:`guides/unreal-set-design`
#. :goto:`guides/bmpcc-timecode`
#. :goto:`guides/bmpcc-to-braw`
#. :goto:`guides/braw-to-resolve`

Production
----------

#. :goto:`guides/unreal-ocio`
#. :goto:`guides/lens-distortion`
#. :goto:`guides/unreal-composure`
#. :goto:`guides/unreal-take-recorder`

Post-Production
---------------

#. :goto:`guides/unreal-to-nuke`
#. :goto:`guides/unreal-to-resolve`
#. :goto:`guides/nuke-depth-of-field`
#. :goto:`guides/nuke-to-resolve`
#. :goto:`guides/resolve-to-nuke`
