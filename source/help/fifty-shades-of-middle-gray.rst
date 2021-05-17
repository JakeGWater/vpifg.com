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

Unreal uses [sRGBLinear]_, so do we need another graph?
We could, but Linear sRGB and ACES are both linear, and neutral colors are identically encoded.

That is, `r=0.18, g=0.18, b=0.18` is the same in ACES and Linear sRGB.



.. [ACES_SPEC] https://acescentral.com/aces-documentation/