==============================
Unreal Composure
==============================

.. topic:: Pre-Requisites

   * :doc:`unreal-ocio`
   * :doc:`bmpcc-hdmi-srgb`

.. topic:: Lesson Plan
   
   We are going to setup Composure in Unreal to take in a live camera feed,
   compose it with a CG scene, and send the combined out over SDI.

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
We will use sRGB in our example by having the BMPCC transform the outgoing HDMI signal via a LUT.

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

      Say hello to our head-model Bob.

#. Test your timecode by recording a short clip.

   .. figure:: https://i.postimg.cc/qR2GqJq0/image.png

   .. figure:: https://i.postimg.cc/gJbvfCD7/image.png

   The timecode won't show up until you play back the recorded clip.
   You should see the timecode from your camera appear under the *In* and *Out* labels.

   .. figure:: https://i.postimg.cc/LXhpFW8z/image.png

      Bob has never looked happier!

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
     - You might be outputting sRGB-linear or ACES instead of sRGB.
       Check the LUT being used by the camera.
   * - The video looks dull or washed out.
     - Incorrect color space.
     - You might be sending the Blackmagic Film color space over SDI.
       Unfortunately that color space is not in OCIO, and Unreal does not know how to convert it.
       Try enabling a Film-to-sRGB LUT on the HDMI signal.
   * - The device cannot be selected because it is greyed out.
     - Another application is using the video input.
     - Ensure Unreal or another app isn't using the SDI connection.

Media Source Setup
==================

#. Create a new **Media Bundle**

   .. figure:: https://i.postimg.cc/4dT0cmgd/image.png

#. Double click the bundle to configure it.

   .. figure:: https://i.postimg.cc/GtgzXpZv/image.png

#. Add a Blackmagic Media Source.

   .. figure:: https://i.postimg.cc/d0MBDp2m/image.png

#. Choose the settings which exactly match your camrea feed.
   For ours, we are shooting at 24fps. 
   Despite recording at 4k the HDMI output is only 1080p.

   .. figure:: https://i.postimg.cc/vZ5P7GHS/image.png

#. Drag the media bundle into your scene.
   It doesn't matter where. We are just testing that it works.
   You should see your camera feed appear on the plane you just dragged in.

   .. figure:: https://i.postimg.cc/d193Gkzt/recording.gif

#. If the media isn't playing, try clicking **Request Play Media** in the details panel.

   .. figure:: https://i.postimg.cc/hvWqJnYJ/screenshot-2.png

Composure
=========

#. Ensure the composure tab is visible

   .. figure:: https://i.postimg.cc/fLbVHcW7/screenshot-3.png

#. From the composure tab, right-click to create a new comp and choose **Empty Comp Shot**.
   Name it anything you like.

   .. figure:: https://i.postimg.cc/FRqy5rKB/screenshot-4.png

The composure actor serves as a container for our other components which will be added together to make the final output.

Media Plate
===========

The **Media Plate** is how we add our camera input to the composure.

#. Right-click the comp and *Add Layer Element*. Choose Media Plate.

   .. figure:: https://i.postimg.cc/zDCv1D3H/screenshot-5.png

#. In the media plate details panel, under ``Inputs > MediaSource > Media Source`` find the texture created with your media bundle.
   You should be see a copy of the live video in the texture thumbnail.

   .. figure:: https://i.postimg.cc/0jn9KQJt/screenshot-7.png

OCIO Input Transform
--------------------

#. Before keying, we need to convert the sRGB footage into sRGB-linear.
   Add a new transform pass, and move it to the beginning before *Multi Pass Chroma Keyer*.
   
   #. Choose **Compositing Open Color IOPass**, and select your OCIO config.
   #. Under Source Color Space, choose the color space your HDMI feed is using, in our case it is sRGB.
   #. Under Destination Color Space, choose ``Utility - Linear - sRGB`` the Unreal Engine color space.

   .. figure:: https://i.postimg.cc/DzrHwNG6/screenshot-8.png

.. important::

   It is handy to have a color chart to see if your colors look right.
   If not, you may have a break in your color pipeline.
   Fix it now.

Chroma Keying
-------------

The next step is keying out the green screen.
In the :doc:`/workflows/BURN`, the composure output we are creating is a sort of "proxy".
We capture the live composure, which allows our editor to get started immediately,
but the proxy will be replaced by a higher quality render later.

We will key out our 4K footage again in Davinci Resolve,
so the keyed footage in this section only needs to be *good enough*.

#. Use the **Multi Pass Chroma Keyer** transform to remove your green screen.

   .. figure:: https://i.postimg.cc/cJv7Dtxn/screenshot-9.png

#. Despill helps remove any green color which has reflected back onto your subject. 

   .. figure:: https://i.postimg.cc/yxW4rTGH/screenshot-10.png

#. Erode trims the fringes of your subject, letting you create a crisper edge.

   .. figure:: https://i.postimg.cc/ZYQ15pgW/screenshot-11.png


CG Plate
========

#. In the composure tab, right-click the comp and add another layer element. Choose **CG Layer**.
   You should see two layers to your comp, a media platae, and a cg element.

   .. figure:: https://i.postimg.cc/kg5VnrtN/screenshot-12.png

The CG layer adds a camera to your scene.
Point your camera at whatever you want.
We are going to overlay the media plate and CG layer.
This will insert the live actors into the CG scene seen by the camera.

If you want to add motion see :doc:`unreal-vive-livelink`.

Composition
===========

#. Select your comp, and in the details panel under ``Transform Passes`` add a transform pass.

   #. Leave the default type as ``Compositing Element Material Pass``.
   #. Create a new material, and save it anywhere.

   .. figure:: https://i.postimg.cc/Gm9pWkZq/screenshot-13.png

The material we just created is in charge of combining the layers of the comp.
Open the material editor to edit the material. We want it to look like this eventually:

.. figure:: https://i.postimg.cc/T1ZkTjtg/screenshot-14.png

#. Add two ``TextureSampleParamater2D`` nodes.

   #. Name the first *exactly* the same name as your media plate.
   #. Name the second *exactly* the same name as your cg element.

   .. warning::

      If your names don't match exactly, it won't work.

   #. Combine the *RGBA* channels with an *Over* node.
      Ensure the media plate is on top, since it contains an alpha layer (from the keyer).
   #. After combining, we have to mask out the alpha layer, or the Blackmagic Media Output will complain.
      Attach the Over node's output to a new *Component Mask* node.
      In the details panel, ensure only *R*, *G*, and *B* are selected.

      .. figure:: https://i.postimg.cc/fyj6qrzk/screenshot-17.png
       
   #. While selecting the output material, under the details panel change *Material Domain* to *Post Process*.

      .. figure:: https://i.postimg.cc/YqCgSL5m/screenshot-15.png
   
   #. Attach the mask output to the emissive color. 

      .. figure:: https://i.postimg.cc/T1ZkTjtg/screenshot-14.png

   #. Click on the comp to see a preview of the combined layers.

      .. figure:: https://i.postimg.cc/m2KDGcB4/screenshot-16.png

Garbage Matte (Optional)
========================

Media Output
============

OCIO Output Transform
---------------------


Disable Tonemapping
-------------------

