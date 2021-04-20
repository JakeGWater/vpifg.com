:author: Jake G. Water
:date: 2020-04-19

=================
HDRI From Scratch
=================

.. topic:: Pre-Requisites

   #. :guilabel:`Optional` :doc:`sekonic-camera-calibration`
   #. :guilabel:`Optional` :doc:`lighting-ev-primer`

.. topic:: Lesson Plan

   #. Required Equipment
   #. How to Captue in the Field

      #. Choosing a Spot
      #. Light Meter Measurements

         #. Estimating Light

      #. Camera Settings
      #. Calibration Photos
      #. Brackets
      #. Extreme Light Sources

         #. The Sun is Very Bright

      #. Second Calibration Photos

   #. Processing Raw Photos in [CaptureOne]_ and [ColorChecker_Camera_Calibration]_
   #. Stitching Using [PtGui]_

Equipment
=========

#. Canon EOS 5D Mark III
#. Magic Lantern
#. Tokina SD 17-35 F4 (IF) FX
#. Sekonic L-858D-U
#. X-Rite ColorChecker Passport 2
#. Tripod
#. Panoramic head
#. Nisi 3,6,10-stop Filters and V6 Mount

Equipment Setup
===============

[Optional] Calibrate Your Light Meter 
-------------------------------------

See :doc:`sekonic-camera-calibration`

Removing Parallax
-----------------

* https://www.bhphotovideo.com/explora/photography/tips-and-solutions/tools-of-the-trade-for-panoramic-photographers

Capturing
=========

Choosing a Spot
---------------

Light Meter Measurements
------------------------

We are going to import these haris into our Unreal environment later.
The more explicit light measurements we have about the scene the better.
This will help us choose the right settings on the unreal side to make the lighting match.

Estimating Light
----------------

Before setting up your camera, you need to profile the light of your scene.
This includes every light source, in every shadow.
You want to get an idea of the brightest light and the darkest dark, in order to ensure that your brackets capture everything.

For some things, you can just point your light meter at it and read the value directly.
The light meter will tell you what camera settings you need to use.

Your camera can also tell you if anything in the scene is clipping.
Take a few test photos with the recommended settings from your light meter, and look to see if anything is clipping or underexposed.
Ten to fifteen minutes now will save you a lot of time later.

Estimating the Sun
^^^^^^^^^^^^^^^^^^

If you have strong enough ND-Filters, at least 19 stops, you can probably capture the sun directly.
There are few ways to indirectly estimate the intensity of the sun.

.. danger::

   **Do no look at the sun directly, especially through a viewfinder or the light meter.**

If not capturing directly, you can use one or more of the following approaches.

#. Take an illuminance (*lux*) reading with your meter, pointed at the sun. Multiply the lux value by 13,000.
#. Estimate from your 18% gray card.
   
   Position your grey card directly facing the sun.
   Take a luminance reading (*cd/m2*) of your gray card, and use the formula

   .. math:: L_{sun} = 13000 \frac{L_{card}}{0.18}\pi

#. Guess using charts.
#. Use :math:`1.6e9 cd/m^2`

Calibration Photos
------------------

Brackets
--------

Using magiclantern, the camera can take 12 bracketed shots from a single press.

- Set the camera to take 12 bracketed shots
- Set the bracketing order to ``0, +, ++``

This will bracket the shots in increasing order, which will make it much easier to view when you are examining four hundred photos later in the file explorer.
You will have to set your camera to begin taking photos at the most-underexposed setting.

- Lock the shutter up, to prevent excess wobbling and wear.
- If you don't have a remote trigger, use the 2-second countdown to trigger the shutter.



Extreme Light Sources
---------------------

Equip your ND filters, try not to move the camera.

.. warning::

   Do not change any bracketing settings. Add the filters only. PtGui will get upset if the bracketing values change and refuse to create your HDRI.


The Sun is Very Bright
^^^^^^^^^^^^^^^^^^^^^^

If you plan on capturing the sun directly, the camera needs to be able to catpure 33EV.
From [Wiki:EV100]_ given :math:`N` as the apeture and :math:`t` as shutter speed, then EV can be calculated as:

.. math:: EV = \log_2 \frac{N^2}{t}

Or reversing that with :math:`EV=33` and apeture f/8 we get:

.. math:: t = \frac{N^2}{2^{EV}} = \frac{1}{134217728}

That's an impossible shutter speed. Even for f/32 we would need a shutter speed of 1/17747798.
There is no way to capture the sun without *very strong ND filters*.
For f/8 and 1/8000 shutter speed, a camera can capture EV18.96, thus we need 33-19 = 14-stops of filters.

The NiSi filters provide 10, 6, and 3 stop filters which can be stacked giving a total of 19 stops, *perfect*.

.. [Wiki:EV100] https://en.wikipedia.org/wiki/Exposure_value

Second Calibration Photos
-------------------------

Post-Processing
===============

Processing Raw Photos
---------------------

PtGui can process most Raw files directly, but as an option we can use [CaptureOne]_ to apply an calibrated ICC profile to the Raw files and save them as 16-bit TIFFs.

.. sidebar:: Generating an ICC Profile

   .. raw:: html

      <iframe width="100%" src="https://www.youtube.com/embed/FxW7tN6FNh0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#. White balance using your calibration photo. You can apply this to all further Raw files.
#. Crop and extract the calibration photo of your color chart, after white balancing. 

   #. Apply an empty ICC profile
   #. Export as a 16-bit TIFF with embedded ICC profile.

#. Use [ColorChecker_Camera_Calibration]_ to generate an ICC profile.
#. Back in CaptureOne, apply white-balance, and the generated ICC profile to the 300+ bracketed shots of your HDRI. Stay in linear space.
#. Export as 16-bit TIFFs.
#. Use these TIFFs in the next section.


Creating the HDRIs
------------------

#. Drag all your bracketed shots into PtGui.
#. PtGui should recognize that your are trying to create an HDR photo and offer go group bracketed photos.
#. Adjust the EV for any brackets which had filters applied to them.

.. [PtGui] https://www.ptgui.com/

   PtGui Pro is required for stitching HDRIs

.. [CaptureOne] https://www.captureone.com/

.. [ColorChecker_Camera_Calibration] https://xritephoto.com/ph_product_overview.aspx?ID=2632
