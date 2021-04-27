==============
Color Pipeline
==============

.. wip::

.. epigraph::

   If you have spent any time learning about color management,
   you will probably agree that it feels overwhelming.
   This is our attempt at a framework for understanding color that can be built upon.

.. note::

   This content is probably a poor first introduction to color management.
   Instead, it is tareted at folks who have sporradic knowledge,
   but have difficulty remembering how to tie it all together.

   There are a lot of good introductions to ACES and Color Management that already exist,
   and we prefer linking to those whenever possible.

   This video is a great place to start:

   .. youtube:: https://www.youtube.com/embed/NU0P1w5tfHQ

Abstract
========

Our goal with a framework is to keep it simple enough to remember,
but complete enough to be useful.
The consequence of this is that frameworks tend to be a bit abstract,
since they need reduce an infinite variety of workflows into a common set of steps.

Our framework, all of it, is described by the following diagram:

.. svgbob::
   :align: center

   ┌────────┐   Capture   ┌──────────┐    Import    ┌─────────┐
   │        ├────────────►│          ├─────────────►│  Working│
   │ Device │             │ Encoding │              │         │
   │        │◄────────────┤          │◄─────────────┤ Space   │
   └────────┘   Display   └──────────┘    Export    └─────────┘

Where each of the terms in the diagram has a meaning below:

Terminology
-----------

Device
   **Devices always involve light.**
   A Device is a real physical thing, like a camera, TV, monitor, or projector. 
   Display Devices convert electrical signals into illuminated pixels.
   Capture Devices convert incoming light to electrical signals.

Encoding
   **An encoding is transferable digital information.**
   It can be recorded to a file, or sent over a wire.
   Internally there are a lot of characteristics to encodings,
   but we will refer to each permutation as its own encoding.

Working Space
   **Working Spaces are Temporary.**
   A working space imports, combines, manipulates, and exports encodings.
   Working spaces must deal with importing multiples encodings,
   and transforming them such that they can work together.

Examples
--------

Everything film, tv, and video production setup fits into the above pattern.
Let's look at a few examples:

#. Record using a BMPCC and save the video as a RAW file.

   In this example, the BMPCC is the device specifically a capture device. The camera measures the light coming into the sensor, and assembles that into a single frame of image data.
   The RAW file, in thise case BlackmagicRaw is an encoding.
   Every number in the file corresponds to a specific real-world color.
   Internally the BMPCC knows how to convert between the sensor and file.
   In this example there is no working space.

#. Record using a BMPCC and output an HDMI signal to a nearby monitor.

   In this example there are two devices, and one encoding.
   the BMPCC it is a capture device, and the monitor is a display device.
   The HDMI signal carries an encoding over it.
   Importantly the encoding is not just the numbers sent via HDMI itself,
   but the color space represented by those numbers.
   
   If the BMPCC outputs an sRGB signal over HDMI,
   we consider it a different encoding from assuming another color space.

#. A BMPCC saved to a file, then editied in Davinci Resolve.

   In this example, there is one device, one encoding, and one working space.
   The BMPCC captures the incoming footage and saves it to a BRaw file encoding.
   The file is imported into Resolve's working space.

Encodings
---------

Encodings are at the center of the diagram,
and they are extremely important to the color pipeline.

.. sidebar:: Encodings are Like Languages

   Encodings are a broad agreement about what numbers refer to what colors,
   in the same way that a language is a broad agreemnt about what words/sounds refer to what objects.
   When you get your encodings wrong,
   it can be like trynig to read French text expecting english.

This leads to a key takeaway:

.. important::

      If you know the exact encoding of image data, you can reproduce the colors correctly.

And there is an important corollary:

.. danger::

      If you know the exact encoding of image data, you *cannot* reproduce the colors correctly

.. sidebar:: Chips Please

   Just like the word *chips* sounds correct in the US eng UK,
   but the underlying meaning is different.
   These subtle errors are much harder to notice,
   which is why we realy on a framework to tell us when we need color management and how to do it.

Every encoding, ultimately, is a bunch of numbers. 
Those numbers describe sub-pixels, which togeth form pixels, which together form images, which together form videos.

Each number represents one subpixel. 
Typically three subpixels per pixel: one red, one green, and one blue.
Not always, but usually.
The numbers can be compressed, squeezed, rearranged, etc but it's always one number per subpixel.

In many ways, getting an encoding *really wrong* is preferable because it's easy to spot.
Subtle errors are more deciving, like the differences between US English and UK English.
An sRGB file encoded with a 2.4 gamma curve looks almost right under a 2.2 gamma curve.


Color Management
================
   
.. important::

   Color management is needed any time you move into or from an encoding.

   #. Device color management is accomplished via Calibration, specifically either
      
      #. Display Calibration, or
      #. Capture Calibration.

   #. Working Space color management is accomplished via Transforms.
  
Display Calibration
-------------------

Calibration requires the use of special calibration equipment.

.. sidebar:: Let's Split a Pie

   Calibrations are more like adapting to regional dialects than new languages.
   In the US, "pie" might refer to pizza, a sweet pastry, or a savory pastry.
   When meeting a new friend,
   you might ask them to order a "pie" and see what you get.

   You give them some information, a word, and see what real-world thing you get back.
   
   *That is display calibration.*


A display device is often calibrated with a device like the x-Rite iDisplay Pro,
where software feeds in a bunch of numbers to your display then exactly measures what light the display generates.
The software then *calibrates* the display by "fiddling with the numbers" until the outputted light looks correct.
It saves the data for re-use as a Look Up Table (LUT).

#. For computers, the LUT is usually saved into an ICC profile and used directly by the OS software.

   In this case, the computer does not output a true sRGB signal 
   but a slightly modified one such that the monitor *appears* to correctly display sRGB.
#. Some displays are *hardware calibratable* and store the LUT within the hardware device.

   In these cases, the computer ouputs a true sRGB signal.
   Interally the display applies the LUT before sending the data to the panel.

Capture Calibration
-------------------

A capture device also needs calibration, usually with a device like the [X-RiteColorCheckerVideo]_.
Similar to above,
we use softare to process a content which contains an image of our color checker.
The true values of each color swatch are already known to the softare,
so when examining the image if those colors are different it can calculate the necessary corrections.

In our languages example,
this would be like showing your friend a rounded cheese'n tomato-sauce dish and asking what they call it.
You feed in a real-world item, and ask for the information they use to describe it.

Corrections generated by calibration software are stored as LUTs.
LUTs are necessary if one wishes to transform from one encoding to another.
In our abstract model,
it is worth highlighting a distinction between "this is an 8-bit sRGB" encoding,
and the more abstract "this file contains enough information to assign the correct color to every pixel" encoding.

#. Some cameras can be hardware calibrated. 
   They will apply the corrections your calibration softawre generates before encoding the file.
#. Most of the time, corrections are applied in a *Working Space* like Davinci Resolve.

.. important::

   We must treat all files, even files shot with the same camera, as different encodings.
   At least until the color calibration corrections have been applied.
   
Remember how we said two encodings were different unless *all settings* were identical.
We treat the calibration as part of the encoding.

#. For multiple takes, only one calibration is often necessary.
   We would refer to the files from all those takes collectively as having the same encoding.
#. If two separate files were recorded to the same file-format with the same settings,
   and each was captured on a hardawre calibrated camera then we say they have the same encoding.

.. rubric:: Lets take a look at two examples:

1. Meg is filming two scenes on the same [RED]_ camera. One scene is indoor and the other is outdoor.
   Both scenes are saved as [RedcodeRaw]_ files with the same settings aside from ISO, f-stop, and focal length.
   
   Before each scene, Meg records a few seconds of an x-Rite Color Passport checker.

   *Are all these files the same encoding?*

   No. It is reasonable to assume all takes in a scene are the same encoding,
   since they were filmed under the same conditions.
   However, there are enough differences between the indoor and outdoor scenes that we should assume a significantly different calibration is required.
   Thus there are two encodings: one from the indoor scenes, and one from the outdoor scenes.
2. Tom has a two camera live TV broadcast.
   At the beginning of every day, Tom takes a color checker to each camera and generates a correction from test footage such that the cameras output a Rec.709 signal over SDI.

   *Do these SDI cables carry the same encoding?*

   Yes. We say these cables have the same encoding because they originate from hardware calibrated cameras.
   The cameras apply a correction to their output based on real world calibration. 

As you can see, these different examples both fit within our abstract framework.
Further, we can use that framework to ensure we maintain our color pipeline.
In Meg's example, we use our framework to tell us that footage from the two scenes cannot be combined until we have applied color correction.

Working Space Transforms
------------------------

Transforms are just as important as calibration,
but are more math and book keeping than measuring.

.. sidebar:: It's all Legalese to Me

   There's a reason contracts are written in a style of english that otherwise unpalatable.
   As we have already seen, every day english is full of ambiguities, and assumptions.
   Legalese exists to answer the question "What exactly did we agree to".

   In other words, legalese is your *working space*.

Working spaces *import* one or more encodings.
The encodings might all be different.
Either saved into different file formats,
saved in different color spaces,
or saved before color correction has been applied.
In any case, simply combining the numbers stored in each file will rarely if ever work out.

Before combining, the numbers from each encoding need to be transformed such that they all mean the same thing.
Think of this like another *internal* encoding used by the working space.
It doesn't matter because you never need to know the encoding, as long as your transforms know what to do.

.. rubric:: Example

Meg, wanting to edit the footage from her two scenes imports those files into Resolve,
which has been set to use ACES color management.
Immediately after importing, no transforms have yet been applied.
Meg clicks each file, and sets the appropriate Input Device Transform (IDT) which informs Resolve which color space the file is using.
Resolve takes care of the rest.

The files will be automatically converted to the internal ACES space when added to a timeline. 

One more step though.
Remember that Meg filmed two scenes with two different calibrations.
Resolve does not know to apply any color correction automatically,
but Meg can then go through each file and apply the color correction LUTs generated by the calibration software.

After correction, Meg can freely combine her footage without worrying about potential color problems.

Summary
=======

We don't expect you to completely understand color management if this is your fist encounter with it.
Rather, if you've struggled with how it all fits together, then we hope this framework helps you see the whole picture.

A great next step is diving into the details.
