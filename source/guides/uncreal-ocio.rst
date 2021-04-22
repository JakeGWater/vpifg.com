====================
OCIO Setup in Unreal
====================

.. topic:: Lesson Plan

    #. What is OCIO?
    #. How to Download
    #. Configuring in Unreal

.. wip::

Any time footage leaves the camera and enters your computer, or your video files move between programs, we need to think about the color pipeline.
We need to know:

1. What color space the footage is coming from, and
2. what color space the footage is going to.

Mapping between color spaces is easy, usually, thanks to OCIO.
OCIO can be somewhat confusing, but in short it is:

1. A catalog of common color spaces.
2. A set of tools for converting between those spaces.

To use OCIO in Unreal, we need to tell Unreal where to find the catalog, and then which color spaces we wish to use.


Downloading OCIO
================


Configuring Unreal
==================

#. sRGB Linear
#. ACES 2065-1
#. ACEScg
#. Rec.709
#. sRGB

