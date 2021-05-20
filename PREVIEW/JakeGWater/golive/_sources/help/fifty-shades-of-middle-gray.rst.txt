===========================
Fifty Shades of Middle Gray
===========================

.. milestone::

It might be easiest to start at the end.
What does sRGB consider middle gray?
Middle gray is usually "What humans consider to be halfway between black and white".
One might think, on a scale of 0 being black and 1 being white that middle gray is 0.5.
In reality, we tend to think of values near 0.18 as *middle*.

In other words, a neutrally colored diffuse material with 18% reflectivity should be *middle gray*.
ACES event codifies this into their spec [ACES_SPEC]_.

sRGB
====

We can deduce *middle gray* in other color spaces using OCIO.
By inputting 0.18 from the ACES color space, we can check the output values in other color spaces.

For example, we plot the interval 0 to 1 going from ACES to sRGB.

.. figure:: https://i.postimg.cc/VvsjZ50D/Plot-ACES-to-s-RGB.png

   The plot of exposure values from ACES to sRGB:

Thus sRGB has a middle gray value of 0.36 on the interval [0,1]. On a scale of 0-255 this would be 92.
So `rgb(92,92,92)` in sRGB is middle gray.

sRGB Linear
===========

Unreal uses Linear sRGB, so do we need another graph?
We could, but Linear sRGB and ACES are both linear, and neutral colors are identically encoded.

That is, `r=0.18, g=0.18, b=0.18` is the same in ACES and Linear sRGB.

Blackmagic Raw
==============

Unfortunately there are no OCIO config files for Blackmagic Raw,
but DaVinci Resolve can generate a *Blackmagic Film Gen 4 to ACES* LUT for you.

.. figure:: https://i.postimg.cc/cCsdmyDC/Plot-Blackmagic-Pocket4k-Film-to-ACES.png

   The plot of exposure values from Blackmagic Raw using the Pocket 4K Film color space to ACES.

As we can see, the value for *middle gray* is 0.38.
Luckily, according to the following source, 0.38 coincides exactly with *green* when using false color mode.

.. youtube:: https://www.youtube.com/watch?v=ToUeatbx9Lo

Putting it all Together
=======================

If you are combining Unreal footage with camera footage,
you will want your gray values to be set correctly at the source.
When applying any OCIO transforms, the gray values from your different sources will match up exactly when combined.

..
   https://github.com/ampas/aces-dev/blob/master/transforms/ctl/README-MATRIX.md
   https://github.com/microsoft/vcpkg#quick-start-windows
   https://github.com/OpenImageIO/oiio/blob/master/INSTALL.md#installing-from-package-managers

.. [ACES_SPEC] https://acescentral.com/aces-documentation/
