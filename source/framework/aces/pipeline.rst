==============
Color Pipeline
==============

.. wip::

Maintaining your color pipeline is extremely important.

.. note::

   This section intends to be read more like a reference than an introduction.
   There are a lot of good introductions to ACES and Color Management that already exist,
   and we prefer linking to those whenever possible.

.. sidebar:: Color Management, Color spaces and Gamut

   .. raw:: html

      <iframe width="560" height="315" src="https://www.youtube.com/embed/NU0P1w5tfHQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Abstractly, will to refer to all aspects of color management as fitting within the following framework.

.. svgbob::

   ┌────────┐   Capture   ┌──────────┐    Import    ┌─────────┐
   │        ├────────────►│          ├─────────────►│ Working │
   │ Device │             │ Encoding │              │         │
   │        │◄────────────┤          │◄─────────────┤  Space  │
   └────────┘   Display   └──────────┘    Export    └─────────┘

Davice
   A Device is a real physical thing, like a camera, TV, monitor, or projector. 
   Display Devices convert electrical signals into illuminated pixels.
   Capture Devices convert incoming light to electrical signals.

Encoding
   And encoding is a digital signal.
   It can be recorded to a file, or sent over a wire.
   Internally there are a lot of characteristics to encodings,
   but we will refer to each permutation as its own encoding.

Working Space
   A working space is used to manipulate image data, such as a video or photo.
   Working spaces import encoded content, manipulate it, then export it.

Everything related to color management fits into this abstract pattern.
Let's look at a few examples:

#. Use a BMPCC to record a video as a RAW file.

   In this example, the BMPCC is the device specifically a capture device. The camera measures the light coming into the sensor, and assembles that into a single frame of image data.
   The RAW file, in thise case BlackmagicRaw is an encoding.
   Every number in the file corresponds to a specific real-world color.
   Internally the BMPCC knows how to convert between the sensor and file.
   In this example there is no working space.

#. Use a BMPCC and output an HDMI signal to a nearby monitor.

   In this example there are two devices, and one encoding.
   the BMPCC it is a capture device, and the monitor is a display device.
   The HDMI signal carries an encoding over it.
   Importantly the encoding is not just the numbers sent via HDMI itself,
   but the color space represented by those numbers.
   
   If the BMPCC outputs an sRGB signal over HDMI,
   we consider it a different encoding from transmitting a Filmic color space signal.

Here is the problem.
Each of these files and programs uses numbers to describe the colors in its scene.

For example sRGB uses three numbers to describe the color of each pixel.
One for the amount of red, green, and blue respectively between 0 and 1.
The reddest red, for example, would be ``(1, 0, 0)``.
The greenest green would be ``(0, 1, 0)``, and the bluest blue is ``(0, 0, 1)``.

Unfortunately the color ``(1, 0, 0)`` in sRGB might be very different from the color represented by ``(1, 0, 0)`` in BRaw-Film.
There are other challenges:

#. Different spaces has different ranges. 
   While sRGB numbers are between 0 and 1, an ACES number is between 0 and 65504.
#. Colors can *get brighter faster* in different color spaces. 
   The rate can even change within a color space (this is what gamma/log stuff does).
   If you double an ACES color, it gets twice as bright so we call that linear.
   In sRGB, doubling the value 0.1 to 0.2 does not make the pixel twice as bright.

Copying the files between these color-spaces without proper conversion will skew the colors away from their original values.
Any time we change color spaces, we need to **transform** the values.
For example, if we have Braw-Film value of 0.25 we need to figure out what the equivalent ACES number is that represents the same color.

There are a lot of names for these transforms:

#. IDTs (Input Device Transforms)
#. ODTs (Output Device Transforms)
#. LUTs

However not all LUTs are actually color transforms.
In fact most are not.
The LUT needs to have been specifically designed to changes colors from a specific color space into another.

It gets worse.
If color spaces are buckets, different buckets are different sizes.
Some, like ACES, can hold more colors.
The sRGB bucket is one of the smaller buckets.
So what happens if we try to convert from ACES to sRGB?
The extra colors spill on the floor.

File Encoding
Color Primaries
Gamma Curves
Bit Depth

In theory, any of these are interchangable.
In practice, there are only a few combinations you are going to encounter.

Here are the ones to remember.

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


An unbroken color pipeline means accounting for each of these changes at every step. 
Generally, if your footage looks washed out, too dark, or otherwise bad you likely have a break in your color pipeline.

.. warning::

    LUTs cannot undo a broken color pipeline, no matter how hard you try.

A deep dive on color is beyond This article's current scope.
All you need to keep in mind is that any time you move footage from  one step to the next,
the color pipeline is involved.
For every workflow we discuss, we should consider how to maintain the color pipeline.
