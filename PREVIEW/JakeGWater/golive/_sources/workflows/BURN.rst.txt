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
It is designed to be small, cost-efficient, but able to achieve high-quality output.
BURN is a compromise between mixed-reality and traditional green-screen workflows. 
BURN has two pieces:

1. All equipment records internally at its highest quality.
2. A lower-fidelity live-composite is captured, viewable, and recorded on-set during the shot.

The lower quality capture is immediately available for editing, and contains all the final vfx, but without any post-processing polish that may be applied.
After editing, the higher quality footage may be substituted in using timecode to insert any clips into their correct spot in the timeline.

.. rubric:: Illustsrated Workflow

.. figure:: https://i.postimg.cc/HLM1Wr48/screenshot-52.png

Guides
======

.. figure:: https://i.postimg.cc/MpGXKJTJ/screenshot-53.png

1. :goto:`guides/bmpcc-to-braw`
   :goto:`guides/braw-to-resolve`
2. :goto:`guides/bmpcc-timecode`
3. :goto:`guides/unreal-vive-livelink`
4. :goto:`bmpcc-hdmi-srgb`
5. :goto:`guides/unreal-composure`
   :goto:`guides/unreal-ocio`
   :goto:`guides/lens-distortion`
6. :goto:`guides/decklink-loopback-recording`
7. :goto:`guides/unreal-take-recorder`
8. :goto:`guides/unreal-to-nuke`
9. :goto:`guides/nuke-depth-of-field`
10. :goto:`guides/nuke-to-resolve`

Extras
------

#. :goto:`guides/unreal-set-design`
#. :goto:`guides/unreal-to-resolve`
#. :goto:`guides/resolve-to-nuke`
