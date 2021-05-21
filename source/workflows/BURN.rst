#################
BURN Workflow
#################

.. prodcheck::
    :4k: yes
    :timecode: yes
    :raw: yes
    :aces: yes
    :ndisplay: no
    :live: yes
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

Guides
======

Each step of the workflow is illustrated below:

.. figure:: https://i.postimg.cc/hP41tsFJ/screenshot-56.png

Please see the corresponding guide for each step:

#. :goto:`guides/bmpcc-to-braw`
#. :goto:`guides/braw-to-resolve`
#. :goto:`guides/bmpcc-hdmi-srgb`
#. :goto:`guides/bmpcc-timecode`
#. :goto:`guides/unreal-vive-livelink`
#. :goto:`guides/unreal-ocio`
#. :goto:`guides/unreal-media-capture`
#. :goto:`guides/unreal-composure`
#. :goto:`guides/decklink-loopback-recording`
#. :goto:`guides/resolve-proxy-editing`
#. :goto:`guides/unreal-take-recorder`
#. :goto:`guides/unreal-movie-render-queue`
#. :goto:`guides/unreal-to-nuke`
#. :goto:`guides/nuke-depth-of-field`
#. :goto:`guides/nuke-to-resolve`
#. :goto:`guides/resolve-relink-media`

Extras
------

#. :goto:`guides/unreal-set-design`
#. :goto:`guides/unreal-to-resolve`
#. :goto:`guides/resolve-to-nuke`
#. :goto:`guides/unreal-lens-distortion`
