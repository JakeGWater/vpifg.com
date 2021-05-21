:author: |jake|
:author_url: |jake.url|
:date: 21/05/2021

============================
sRGB vs sRGBLinear over HDMI
============================

SRGB *looks right* when displayed on a monitor.
Linear sRGB is Unreal's working color space, and thus wouldn't require an input transform in composure.

In a very unscientific test, we processed an sRGB and linear sRGB test pattern through the 10-bit 4:2:0 sub-sampling used by our HDMI connection.

.. figure:: https://i.postimg.cc/X7cm2FF1/screenshot-45.png

Linear sRGB (left) and sRGB (right) after converted to 10-bit and compressed in YCbCr using 4:2:0 chroma sub-sampling.
Test pattern from [RTINGSChromaTest]_.

The sRGB linear appears to fair better in this example.
You can use either color space, as long as you understand the implications of both approaches.
