=================
One Shade of Gray
=================

.. planned::

Fifty Values of Middle Gray
---------------------------

It might be easiest to start at the end.
What does sRGB consider middle gray?
This might vary from display to display, but our *source of truth* is OCIO.

We can use that to deduce our target sRGB gray value.

#. ACES is our color pipeline.
#. We know ACES2065-1 defines middle-gray as 0.18
#. We can use an OCIO transform from ACES to sRGB to determine our target sRGB value.

.. figure:: https://i.postimg.cc/VvsjZ50D/Plot-ACES-to-s-RGB.png

   The plot of exposure values from ACES to sRGB:

According to OCIO on a (0-1) interval sRGB middle gray is 0.36. This would be ~92 on a (0-255) interval.

