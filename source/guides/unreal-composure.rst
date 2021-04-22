==============================
Unreal Composure
==============================

.. topic:: Pre-Requisites

   * :doc:`unreal-ocio`
   * :doc:`bmpcc-hdmi-srgb`

.. contents:: Lesson Plan
   :local:

.. topic:: Next

   * :doc:`bmpcc4k-to-braw`
   * :doc:`unreal-take-recorder`

Camera
======

Connecting
----------

Turn your camera on, and connect it to the Decklink.
We will use a Decklink 8K Pro, but other supported cards should work the same.

.. svgbob::

                                                                                       Decklink 8K Pro
                                                                                       ┌──────────────┐
                                                                                   ┌───┤              │
                                                                                   │   │SYNC          │
                                                                                   └───┤              │
     BMPCC                                                                             │              │
   ┌───────────┐                                                                       │              │
   │           │              Microconverter                                       ┌───┤              │
   │           │              Blackmagic HDMI to SDI 3G               ┌───────────►│   │SDI 1         │
   │           │               ┌───────────────────────┐              │            └───┤              │
   │           │               │                       ├───┐     SDI  │                │              │
   │     Out   │               │                       │   ├──────────┘            ┌───┤              │
   │     HDMI  │               │                       ├───┘                       │   │SDI 2         │
   │     ┌──┐  │    HDMI       │                       │SDI Out                    └───┤              │
   │     │  ├──┼─────┐       ┌─┤                       ├───┐                           │              │
   │     │  │  │     │       │ │ HDMI                  │   │                       ┌───┤              │
   │     └──┘  │     └──────►│ │ In                    ├───┘                       │   │SDI 3         │
   │           │             │ │                       │                           └───┤              │
   │           │             └─┴───────────────────────┘                               │              │
   └───────────┘                                                                   ┌───┤              │
                                                                                   │   │SDI 4         │
                                                                                   └───┤              │
                                                                                       └──────────────┘

.. important::

   To our knowledge, the **Microconverter - Blackmagic HDMI to SDI 3G** is the only supported
   HDMI to SDI coverter that preserves timecode.

Settings
--------

Your camera *must* output a known color space.
We will use sRGB in our example.

See :doc:`bmpcc-hdmi-srgb` on setting up the BMPCC to output sRGB.

.. important::

   Ensure your camera is set to record in its RAW format with full-gamut color space.
   See :doc:`bmpcc4k-to-braw`.
   
   **Do not apply any LUTS to the recorded file**.

Checking It Works
-----------------

Before proceeding, we should check the SDI connection is working.

#. Open Blackmagic MediaExpress.

   .. figure:: https://i.postimg.cc/Vvc4YQLp/image.png

#. Choose the decklink port your camera is connected to

   .. figure:: https://i.postimg.cc/GhZ3bdWq/image.png

#. Switch to the **Log and Capture** tab

   .. figure:: https://i.postimg.cc/QMKyhrrk/image.png

#. You should see your camera, live!

   .. figure:: https://i.postimg.cc/J7Qm9jx7/image.png

#. Test your timecode by recording a short clip, and playing it back.

   .. figure:: https://i.postimg.cc/qR2GqJq0/image.png

   .. figure:: https://i.postimg.cc/gJbvfCD7/image.png

   You should see the timecode from your camera appear under the *In* and *Out* labels.

   .. figure:: https://i.postimg.cc/LXhpFW8z/image.png

.. important::

   If your footage doesn't appear, or the colors look wrong *STOP AND FIX IT*.

Troubleshooting
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :align: left
   :widths: 20 20 60

   * - Problem
     - Caused by
     - Fix
   * - The screen is black
     - No video input
     - Try another decklink port;
       Check all your wiring;
       Ensure you have setup your Decklink correctly in **Desktop Video Setup**.
   * - The video looks dark
     - Incorrect color space.
     - Ensure your camera is outputting sRGB.
       In the BMPCC, ensure your LUT is being applied to the HDMI file.

Media Source Setup
==================


Composure
=========

Media Plate
===========

OCIO Input Transform
--------------------

Chroma Keying
-------------

CG Plate
========

Garbage Matte
=============

Composition
===========

Media Output
============

OCIO Output Transform
---------------------


Disable Tonemapping
-------------------

