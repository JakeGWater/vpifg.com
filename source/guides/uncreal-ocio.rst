====================
OCIO Setup in Unreal
====================

.. topic:: Lesson Plan

    #. What is OCIO?
    #. How to Download
    #. Configuring in Unreal

.. wip::

What is OCIO
============

Any time footage leaves the camera and enters your computer, or your video files move between programs, we need to think about the color pipeline.
We need to know:

1. What color space the footage is coming from, and
2. what color space the footage is going to.

Mapping between color spaces is easy, usually, thanks to OCIO.
OCIO can be somewhat confusing, but in short it is:

1. A catalog of common color spaces.
2. A set of tools for converting between those spaces.

To use OCIO in Unreal, we need to tell Unreal where to find the catalog, and then which color spaces we wish to use.

Where OCIO is Necessary
=======================

There are several places we will need OCIO with Unreal.

#. Blackmagic Media Source Input and Output in Composure.
 
   #. The incoming camera footage must be mapped to *sRGB Linear*.
   #. The outgoing composure will be mapped to *Rec.709*.

#. Movie Render Queue. We will render our footage to ACEScg.


Downloading OCIO
================

#. If you check here [OpenColorIO-103]_ it tells you to go *here* instead [ColourScience-ACES12]_.
#. Download the repository. It's **BIG**, like 5GB.
#. Save it somewhere you can access from Unreal.

.. [ColourScience-ACES12] https://github.com/colour-science/OpenColorIO-Configs/tree/feature/aces-1.2-config
.. [OpenColorIO-103] https://opencolorio.readthedocs.io/en/latest/configurations/aces_1.0.3.html

Configuring Unreal
==================

All OCIO transforms are expressed as *from* some space *to* another space. 
We need to select every space we intend to convert from, as well as every space we intend to convert into.

#. Create an OCIO object.
#. Add the following color spaces:

   #. sRGB Linear - This is the default working space of Unreal. All conversions will either be *from* or *to* this space.
   #. ACES 2065-1 - Not necessarily used, but this is sort of the unviersal color space, and worth having around.
   #. ACEScg - We will render our footage to ACEScg.
   #. Rec.709 - We will convert our live composure output to either Rec.709 or sRGB.
   #. sRGB
