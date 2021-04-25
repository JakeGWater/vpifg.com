==============
Color Pipeline
==============

.. wip::

Maintaining your color pipeline is extremely important.

A very simple pipeline involving a single BMPCC, Unreal, and Davinci Resolve.

.. svgbob::

    ┌────────────┐      ┌───────────────┐
    │            │      │               │
    │  BMPCC     │      │  Unreal       │
    │            │      │               │
    │            │      │               │
    │            │      │               │
    │  BRaw-Film │      │  sRGB-Linear  │
    │     │      │      │      │        │
    └─────┼──────┘      └──────┼────────┘      ┌───────────┐      ┌───────────┐
          │                    │               │           │      │           │
          │                  (IDT)             │  Resolve  │      │  Display  │
        (IDT)                  │               │           │      │           │
          │                    └──────────────►│           │      │           │
          │                                    │   ACES    ├─────►│  sRGB     │
          └───────────────────────────────────►│           │      │           │
                                               │           │      │           │
                                               └───────────┘      └───────────┘

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
If color spaces are buckets, the 

Dynamic Range

Encoding


An unbroken color pipeline means accounting for each of these changes at every step. 
Generally, if your footage looks washed out, too dark, or otherwise bad you likely have a break in your color pipeline.

.. warning::

    LUTs cannot undo a broken color pipeline, no matter how hard you try.

A deep dive on color is beyond This article's current scope.
All you need to keep in mind is that any time you move footage from  one step to the next,
the color pipeline is involved.
For every workflow we discuss, we should consider how to maintain the color pipeline.
