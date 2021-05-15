:author: Jake G. Water

==============================
Unreal Virtual Camera Matching
==============================

.. milestone::

The CineCameraActor in Unreal has a lot of settings that mirror real world cameras.
Those settings when tweaked can affect the image.

Sensor Size
===========

The **sensor size** has a large effect on the final image. 
A smaller sensor acts like a zoom.

#. A full-frame sensor with a 35mm lens:

   .. figure:: https://i.postimg.cc/DwWn7fsG/filmback-c35.png

#. The same camera and lens, but with the smaller Blackmagic sensor: 

   .. figure:: https://i.postimg.cc/Pr5dFQ52/filmback-bm43.png

Focal Length
============

Focal length and sensor size *offset* each other.
A smaller sensor acts like a zoom.
In real-live photography a larger sensor produces a better quality image,
but in digital cinema the sensor size has no effect on quality.

#. The Blackmagic MFT sensor with a 10mm lens:

   .. figure:: https://i.postimg.cc/wMXrDcdH/filmback-left.png

#. A 1000mm lens, but offset with an equally large sensor:

   .. figure:: https://i.postimg.cc/kgXHtbY3/filmback-right.png

   As you can see, the images are identical. The longer focal length is offset by the larger sensor size.

Calculating
===========

.. sidebar:: CropFactorCalculator for BMPCC
   
   .. figure:: https://i.postimg.cc/hjQ2Gwsp/screenshot-32.png

   From [CropFactorCalculator]_

While it is possible to calculate the same image proportions with different settings,
it's far easier to match the virtual camera settings exactly to your real world camera.

The BMPCC4K Sensor Size is: 18.96mm x 10mm for 4K DCI (4096 x 2160).
Since we are recording at UHD (3840 x 2160), it is a little narrower than the full DCI.
We should calculate a new sensor size with the reduced width, but keeping the full height.
So, our new narrower sensor width is:

.. math:: \frac{3840}{4096} \cdot 18.96mm = 17.775mm 

The effective sensor size in UHD is 17.775mm x 10mm.
We should double check this has the same aspect ratio as 1080p, which is the scaled down resolution sent over HDMI.

.. math:: \frac{17.775mm}{10mm} \cong 1.7775 \cong \frac{1920}{1080}

We are using a Metabones Speedbooster 0.71 with a Sigma 18-35mm lens (zoomed to 24mm).
According to [CropFactorCalculator]_ our *Focal Length with Speed Booster* is 32.17mm.

Thus our virtual camera settins are:

#. Focal Length: **32.17mm**
#. Sensor Size: **17.775mm x 10mm**

.. [CropFactorCalculator] https://danielscottfilms.com/crop-factor-calculator/
