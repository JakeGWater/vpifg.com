:author: Jake G. Water
:date: 2021-04-23

==============================
Unreal Composure
==============================

.. wip::

.. topic:: Pre-Requisites

   * :doc:`bmpcc-hdmi-srgb`
   * :doc:`unreal-ocio`
   * :doc:`unreal-timecode-genlock`
   * :doc:`unreal-virtual-camera-matching`

.. topic:: Lesson Plan
   
   We are going to setup Composure in Unreal to take in a live camera feed,
   compose it with a CG scene, and send the combined out over SDI.

.. topic:: Next

   * :doc:`unreal-composure-lighting`
   * :doc:`bmpcc-to-braw`
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

.. note::

   To our knowledge, the **Microconverter - Blackmagic HDMI to SDI 3G** is the only supported
   HDMI to SDI coverter that preserves timecode.

Settings
--------

Your camera *must* output a known color space.
We will use sRGB in our example by having the BMPCC transform the outgoing HDMI signal via a LUT.

.. important::

   See :doc:`bmpcc-hdmi-srgb` on setting up the BMPCC to output sRGB.

While the HDMI signal is 1080p sRGB, ensure your camera is set to record in its RAW format with its widest-gamut color space.

.. important::
   
   See :doc:`bmpcc-to-braw` on setting up the BMPCC to record in 4K RAW.

Check that your camera connection is working :doc:`/help/troubleshooting-decklink`.

Media Source Setup
==================

We use a Media Bundle to connect Unreal to the Decklink.

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

.. important::

   If your footage doesn't appear see :doc:`/help/troubleshooting-decklink` for help.

Timecode and Genlock
====================

Our composure output will output timecode, and use genlock to drive the render frame rate.
Without timecode, the footage you record from composure will not match up with any VFX you render in post-processing.
We want the live composited footage to exactly match the timecode of the raw footage.

.. important::

   See :doc:`unreal-timecode-genlock` on setting up timecode and genlock with the Blackmagic Decklink 8K Pro.

Check that the timecode in Unreal is being driven by your custom blueprint,
and the displayed time matches your camera.
Check that genlock is operating at the desired framerate.

.. figure:: https://i.postimg.cc/wv0msKcD/screenshot-33.png

Virtual Camera
==============

Set your virtual camera to exactly match your real-life camera. 

.. important::

   See :doc:`unreal-virtual-camera-matching` for details on configuring the virtual camera.

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

.. sidebar:: Transform Comparison

   .. figure:: https://i.postimg.cc/DfWQksdx/composure-ocio-comparison.png

      A broken color pipeline can be hard to notice.
      sRGB without an OCIO transform looks *almost right*,
      but it's not nearly as vibrant when compared to correctly transformed footage.

Before keying, we need to convert the sRGB footage into sRGB-linear.
Add a new transform pass, and move it to the beginning before *Multi Pass Chroma Keyer*.

#. Choose **Compositing Open Color IOPass**, and select your OCIO config.
#. Under Source Color Space, choose the color space your HDMI feed is using, in our case it is sRGB.
#. Under Destination Color Space, choose ``Utility - Linear - sRGB`` the Unreal Engine color space.

.. figure:: https://i.postimg.cc/DzrHwNG6/screenshot-8.png

.. hint::

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

In the composure tab, right-click the comp and add another layer element. Choose **CG Layer**.
You should see two layers to your comp, a media platae, and a cg element.

.. figure:: https://i.postimg.cc/kg5VnrtN/screenshot-12.png

The CG layer adds a camera to your scene.
Point your camera at whatever you want.
We are going to overlay the media plate and CG layer.
This will insert the live actors into the CG scene seen by the camera.

If you want to add motion see :doc:`unreal-vive-livelink`.

Composing Layers
================

Select your comp, and in the details panel under ``Transform Passes`` add a transform pass.

#. Leave the default type as ``Compositing Element Material Pass``.
#. Create a new material, and save it anywhere.

.. figure:: https://i.postimg.cc/Gm9pWkZq/screenshot-13.png

The material we just created is in charge of combining the layers of the comp.
Open the material editor to edit the material. We want it to look like this eventually:

.. figure:: https://i.postimg.cc/T1ZkTjtg/screenshot-14.png

Add two ``TextureSampleParamater2D`` nodes.

#. Name the first *exactly* the same name as your media plate.
#. Name the second *exactly* the same name as your cg element.

.. warning::

   If the node names do not exactly match your layer comp names, it won't work.

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

The composure is running! Now we need to send it somewhere to record.
We will route the output through an unused Decklink port.

#. Select the comp in World Outliner, and go to the details panel.
   Add a **Compositing Media Capture Output** Output Pass to the *Composure Outputs*.

   If the *Capture Output* setting is blank, create a new **Blackmagic Media Output** and save it anywhere you like.

   .. figure:: https://i.postimg.cc/fTThvG7J/screenshot-35.png

#. Choose an unused port to output the SDI signal.

   .. figure:: https://i.postimg.cc/mZjvhdxR/screenshot-36.png

#. Make sure to set *VITC* as your timecode format, and *Wait for Sync* if you have genlock enabled.

   .. figure:: https://i.postimg.cc/wvVGyBGF/screenshot-37.png

OCIO Output Transform
---------------------

.. sidebar:: Color Conversion Comparison

   .. figure:: https://i.postimg.cc/76YNRnKM/composure-output-comparison.png

Under the default settings, Unreal applies tone mapping to our image, and sends it out.
We don't want this.
We want to use OCIO.

With the comp selected, go to the details panel.
Next to *Color Conversion* click *Compositing Tone Pass* and change it to **Compositing OpenColor IO Pass**.

#. Select the OCIO Config you have already been using.
#. The source color space is Unreal, which is always Linear - sRGB.
#. The destinataion color space is whatever you want, but we are going to use sRGB.

   .. figure:: https://i.postimg.cc/zvRPVQmB/screenshot-20.png

#. If you view the SDI signal on an sRGB calibrated monitor, it should look correct. 
   Here we have looped our signal back into the Decklink to view the composure output in Blackmagic MediaExpress.

   .. figure:: https://i.postimg.cc/wxGQr2Cf/screenshot-29.png

      We loop back our SDI connection into Blackmagic Media Express to view the output.

   You can use Blackmagic MediaExpress to record the composure output, as it will capture the output with timecode intact.

Final
=====

If you followed every step, great work.
Yu have setup composure with end-to-end *timecode-integrity* and an intact *color pipeline*.

Next, we highly recommend :doc:`unreal-composure-lighting` to get your composure looking its best.