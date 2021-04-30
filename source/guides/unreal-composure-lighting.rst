:author: Jake G. Water
:date: April 29, 2021

=========================
Unreal Composure Lighting
=========================

.. important::

    You can achieve vivid, realistic colors using Composure *without color grading*.

Physical Lighting
=================

Unreal is capable of physical lighting.
That is, you can enter real-world brightnesses for your lights,
and real world settings for your camera.
The result should *look realistic*.

.. figure:: https://i.postimg.cc/XYqz3fxw/screenshot-39.png

    Shot in 70,000 lux with f/22, ISO 100, 24fps, 180° shutter

However, it is not necessary and matching your composited green-screen footage with the render is more important.
We want precise control over the final RGB values generated from Unreal.
It will be easier to minimize the number of nobs to turn, and thus, we are going completely disregard physical lighting.

Before we get started, it's important to understand how Unreal handles color and how that interacts with OCIO.

Linear sRGB
===========

However you choose to light your scene, ultimately a virtual camera is observing the scene and outputting numeric values for each pixel.
Those values make their way to your monitor, which tell the display how bright or dark to make that same pixel.
The journey from Unreal to your Monitor is our Color Pipeline.

.. figure:: https://i.postimg.cc/Bb6NBsjd/Plot-loglog-linear-s-RGB-to-ACES.png

    sRGBLinear and ACES have identical Black, Gray, and White points.

Unreal renders your content in the *sRGBLinear* color space:

#. Each pixel's color and intensity is determined by three numbers, one for *Red*, one for *Green*, and one for *Blue*. e.g. [1, 0.5, 0] means 1 unit of red, 0.5  units of green, and zero blue.
#. Higher numbers are brighter. Lower numbers are darker. So [1, 1, 1] is brighter than [.5, .5, .5]
#. Double the number means double the brightness. (This is only true for linear color spaces, and definitely not true for sRGB). So [2, 2, 2] is twice as bright as [1, 1, 1].
#. When the numbers are all equal, that pixel is *neutral*. It has no color.
   For example [.7, .7, .7] or [10, 10, 10].
#. The value of 0 means none of that color. Three zeros [0,0,0] is the complete absense of light (i.e. absolute black).
#. Theoretically there is no upper limit, but Unreal stops at 100.
   File formats like 16-bit EXR can go up to 65504.



How OCIO Transforms Color
=========================



As in it's possible to not obey them, but in following them other color processing tools will *just work*.

#. Light values are relative. To what? Make them relative to your key light, and 18% gray card.
#. The 18% gray card, when lit directly with the key light, should output 0.18 in sRGBLinear.
#. No diffuse material can be greater than 1. In sRGBLinear land, a 1 means *this object is maximally lit by light*.
   
   #. In practice the most a diffuse object should be is 0.90. 
      A value of 1 is like a theoretical perfectly reflective surface.
   #. Diffuse materials in the key light can never really be 0. 
      The darkest substance still reflects *some* light.
      A good minimum is 0.05.

#. Emissive lights can go above 1. They should. 
   There is no actual limit, although in our above scheme, 
   on a clear day the sun is theoretically 40,000-60,000.

.. important::

    - 0 is black
    - .18 is 18% gray
    - 1 is white
    - >1 is a light source

.. sidebar:: Calculating the Suns value

    For R as reflectivity of the gray card (i.e. R=0.18),
    L as luminance, E as illuminance, 
    and :math:`\mathscr{L}` as the set of all luminance sources.

    .. math::

        L_{gc} = E_{gc}\cdot\pi\cdot R \\
        E_{gc} = \Omega L_{sun}

If you follow the above, then OCIO will nicely tone map your image whenever transforming color spaces.
You should not need to do much if any color correction on the sRGB or Rec.709 image coming out of Unreal.

So what happens if you don't follow the above rules?
Let's take a look at how OCIO maps colors from sRGBLinear to sRGB.

.. figure:: https://i.postimg.cc/gJt5y9Lx/Plot-linear-s-RGB-to-s-RGB.png

    log of sRGBLinear from 0 to 65504 vs. sRGB from 0 to 1.

The way to read this is that OCIO is going to map 0.18 to 0.36 in sRGB. 
The value 1 in Unreal will get mapped to 0.81 in sRGB.
If, in Unreal, your 18% gray card outputs 1 instead of 0.18, 
then *middle gray* will look a lot more like pure white.
Worse still, over half of your colors will be squished into the range of .81 to 1.
You might be able to fix that with color grading, but why not get it right the first time?

The high-level goal in this section is to make the lighting from up to three different sources look like it matches.
Your sources include:

#. your footage,
#. your scene, and 
#. optionally an HDRI.

If there is an exact equation, we have not yet discovered it.
What we have learned:

#. You do not need absolute, or physical lighting units.
   Balancing can (and should) be done on a relative scale.
#. 18% gray cards are essential to balancing light
#. Those VFX chrome/gray balls are also quite useful
#. Your only goal is to get the _output linear-sRGB values_ correct.



The HDRI has likely already been recorded.
Ideally, you have a reference value for 18% gray.


.. math::

    E_{Dir} &= E_{Sun} - E_{Shade} \\
    I_{HDRI} &= L_{Sky} \\
    I_{Sky} &= \frac{E_{Shade}}{L_{Sky}}

.. math::

    \gamma = \frac{18}{100\cdot E_{Sun}}

Notes::

    - Camera Settings
        - Exposure > Metering Mode > Manual
        - Exposure Compensation > 0
        - Apply Physical Camera Exposure [off]
        - NOW `nits` should equal the linear sRGB value
    - Nothing diffuse in your scene should be > 1 unless it it a light source
        - max: 0.95
        - gray card: 0.18
    - Anything in key light
        - min: 0.05
    - HDRIs
        - skylight
        - intensity
    - Directional Lighting
    - Lining up the HDRI
    - Gray Cards
    - Measuring Real Life
    - Adjusting Media Plate Input
    - Measurements to take
        - Directional
        - Indirect
        - 
    - combining video
        - gray value is set to .18
        - white is
