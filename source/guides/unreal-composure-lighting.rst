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


Lighting
========

Live composites can look really nice, indistinguishable from reality.
They can also look noticeably fake.

Poor lighting break a scene.
Green screened actors can look like there standing in front of a flat background, and CG elements can look cartoonish.

The goal of this section is not to discuss how to use lighting to affect mood, direct the viewer, 
or any other artistically motivated cinematographic techniques.
The goal is to have the composite technically good enough that you can spend color grade focused on storytelling,
and not fixing mistakes.

In other words, this section is a technical guide to maintaining the color pipeline through the composited image.
If you think about it, that's not that easy to do.
You are attempting to merge two images, originating in separate color spaces, with different lighting conditions.

Again, we are not concerned with mood, atmosphere, or anything other than providing a good, robust base to color grade from.
A good starting formula is to attempt to composite your scene in the following order:

1. White Balancing
2. Equalizing Dynamic Range
3. Gray Matching

In all of these steps, we will use 18% gray cards, both real and virtual.
Gray cards are your friend.
A color chart and VFX sphere are also super helpful,
but at minimum you will need a gray card.

White Balancing
---------------

While as a director you may choose to tint or off-balance the lighting in your scene,
compositing into a non-white-balanced scene is going to suck.

#. Use your gray card to white balance your camera footage in-camera.
   You can post-process it in Unreal, but doing it in camera is faster and easier to modify.
   The reason to use the gray card is that later we need that gray card to be neutral.
#. An HDRI can *color* your scene off balance.
   That's fine, it will add to the realism of your final image,
   but the time to fix it is now.

   #. In your CG layer, disable color grading override.
      We are going to adjust everything in the virtual camera.

   #. Use the composure preview and hover your mouse over the gray card to get the RGB values.
      If the values are all equal, you are white balanced.
      If they are not, you need to adjust your cameras *White Balance* and *Tint* settings until the RGB values of the gray card are equal.

.. important::

   See :doc:`/help/white-balance-in-lab` on manually white balancing using the CIE.Lab Color Space.

.. highlights::

   White balance is the foundation of the color pipeline



Equalizing Dynamic Range
------------------------

.. highlights::

   Ambient, Direct, Front

Gray Matching
-------------

.. highlights::

   **If you start with a gray card, you end with a gray card.**

.. sidebar:: What happens if there are multiple gray cards, all at different values?

   This could happen if the cards are facing different orientations,
   or are in uneven lighting. What then?

   Not to worry, we are only concerned with *any gray cards we calibrate against*.
   In any one shot, you calibrate against a single gray card only, typically the one normal (facing directly) to the camera.

The life of gray starts at either the physical gray card filmed by your camera, or virtual gray card in Unreal.
It ends at your monitor.
Our goal is that, for whatever color-value your monitor considers middle-gray, 
that any gray cards we calibrate against end up as that value when sent to the monitor.

.. important::

   See :doc:`/help/one-shade-of-gray` to learn about the life of gray values.

In a scene with 1) a green screen actor, 2) a GC set, and 3) an HDRI, there are three gray values we need to pay attention to.
The closer they all match, the better.

Unreal Gray
-----------

#. Create an gray-card material::

   [0.18] diffuse
   [1.00] roughness

#. Add a plane to your scene with the gray card material. 
   Place it geometrically equal to where your real-life actor will stand,
   and face the card towards the camera.
   The plane should correspond to the same location and orientation of the real-life gray card you will use to calibrate the camera footage.
#. Open the composure CG preview.
   You can hover your cursor over any point to inspect its RGB value.

   #. Ensure there is no enabled preview transform.
      We want to view the RGB Linear values, where gray is 0.18.

#. Select the cinema camera attached to your CG layer and set exposure to manual.

   #. Optionally disable physical based settings.
      This makes your camera 1:1 encode nits to RGB value, and can make this step easier.
      When disabled, ISO, aperture, and shutter speed have no affect on the image.

#. Tweak camera and lighting until the gray card reads exactly 0.18.

   #. Camera exposure compensation moves all image values higher or lower.
   #. HDRI intensity brightens the gray-card as well as the HDRI background.
   #. Sky dome intensity brightens gray-card without brightening the HDRI background.
   #. Directional lighting brightens the directional light on your card.

Real Camera Gray
----------------

It is important to setup any lighting to match Unreal before calibrating your camera's gray level.

#. If your camera has false color, you should use that to calibrate your gray exposure.
#. Adjust the aperture until your gray card reads exactly "middle gray".
#. Inspect the 

.. important:: 
   
   See :doc:`unreal-composure-lighting`.


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
