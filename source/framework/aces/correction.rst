=================
Color Correction
=================

.. planned::

ACES files are saved as 16-bit EXRs, with linear gamma.

A Blackmagic Raw file is always a 10-bit custom log curve.

Practical Guid to ACES

#. ACES encodes relative exposure.
   Relative to what you may ask?
   Whatever you decide, really.
   Practically, you should use a color chart to calibrate against your ambient light level.
#. Film an 18% gray catd and set the RGB value to [.18, .18, .18]. Your calibration is done.
#. The RGB value [1, 1, 1] represents a 100% diffusely-reflective material.
   If there was only ambient light in your scene, nothing would exceed an intensity of 1.
#. Emissive light sources can and should exceed 1. How much? 
   It turns out by a lot. 
   There is no real upper limit.
   If your gray card reading is accurate, the exposure value of the light illuminating it would be 3.14.
#. From zero to 18% gray ACES can encode about 12 stops, and 18 stops from 18% to its maximum brightness.

Math bits

#. ACES is an RGB format, where each pixel is made up of three 16-bit half-floats.
   So a pixel contains :math:`16\times3=48` bits.
#. Practically, this gives each color a range between :math:`2^{-14}` to :math:`65504`.
#. This means ACES can encode 65,536 different intensities per color channel.
