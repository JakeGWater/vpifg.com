=================
Unreal OCIO Setup
=================

.. guide:lesson::
   
   Download OCIO and configure Unreal to use OCIO for color management.

.. guide:shownexts::

What is OCIO
============

Any time footage leaves the camera and enters your computer, or your video files move between programs, we need to think about the color pipeline:

#. What color space the footage is coming from, and
#. what color space the footage is going into.

For example, an annotated color pipeline from :goto:`workflows/BURN` looks like:

.. svgbob::
   :align: center

         Raw        ┌──────┐             Raw
      ┌────────────►│  BRaw├───────────────────────────────────┐
      │             └──────┘                                   │
      │                                                        ▼
      │                        sRGB                        ┌───────┐   ACES
   ┌──┴──┐  sRGB    ┌──────┐  Linear   ┌─────────┐         │Davinci├───────►
   │BMPCC├─────────►│Unreal├──────────►│Composure│         │Resolve│
   └─────┘          └──┬───┘           └────┬────┘         │       │
                       │                    │              └───────┘
                       │                    ▼ sRGB             ▲
                       │               ┌────────┐              │
                       │sRGB           │LiveView│              │
                       │Linear         └────────┘              │
                       │                                       │
                       ▼                                       │
                 ┌────────────┐ ACEScg   ┌──────┐  ACEScg      │
                 │Movie Render├─────────►│  Nuke├──────────────┘
                 │   Queue    │          └──────┘
                 └────────────┘

Unreal uses sRGB-Linear internally, but from the above diagram it will also need to convert from and into sRGB, and ACEScg.

OCIO makes converting between color spaces easy. In short OCIO is:

1. A catalog of common color spaces.
2. A set of tools for converting between those spaces.

At each junction in our pipeline, will need to tell Unreal:

#. where to find the OCIO configs
#. what color space we are converting from.
#. what color space we are converting into.

Unreal and OCIO will handle the rest.

Where OCIO is Necessary
=======================

There are several places we will need OCIO with Unreal.

#. Blackmagic Media Source Input and Output in Composure.

   #. The incoming camera footage must be mapped from sRGB to sRGB-Linear.
   #. The outgoing composure will be mapped from sRGB Linera to sRGB or Rec.709.

#. Movie Render Queue needs to map from sRGB-Linear to ACEScg.

Downloading OCIO
================

#. If you check here [OpenColorIO-103]_ it tells you to go *here* instead [ColourScience-ACES12]_.

   .. figure:: https://i.postimg.cc/RZCHwRh2/image.png

#. Download the repository. It's **BIG**, like 5GB.

   .. figure:: https://i.postimg.cc/hGnsNwDv/image.png
   
#. Save it somewhere you can access from Unreal.

Configuring Unreal
==================

All OCIO transforms are expressed as *from* some space *to* another space. 
We need to select every space we intend to convert from, as well as every space we intend to convert into.

#. Create an **OpenColorIO Configuration** from the Content Browser.

   .. figure:: https://i.postimg.cc/CLmNG0Xw/image.png

   Name it whatever you like, then double-click the configuration to edit:

   .. figure:: https://i.postimg.cc/C5yqCPHC/image.png

   Browse to the OCIO configurations you downloaded earlier.

   .. figure:: https://i.postimg.cc/FHbhWPbF/image.png

   Locate your ``config.ocio`` file in the corresponding version, we are using ``aces_1.1``

   .. figure:: https://i.postimg.cc/28Q5M8rf/image.png

#. Add the following color spaces:

   .. figure:: https://i.postimg.cc/Y2xVsJZs/image.png

   ``Utility ▶ Utility - Linear - sRGB``
      This is the default working space of Unreal. All conversions will either be *from* or *to* this space.
   ``ACES ▶ ACES - ACES2065-1``
      Not necessarily used, but this is sort of the unviersal color space, and worth having around.
   ``ACES ▶ ACES - ACEScg``
      We will render our footage to ACEScg.
   ``Output ▶ Output - Rec.709``
      We will convert our live composure output to either Rec.709 or sRGB.
   ``Output ▶ Output - sRGB``
      OCIO will let us use sRGB output also as an input.

This should cover everything we need.
If you use other color spaces, add them to the list.

.. guide:next:: BMPCC4K sRGB HDMI Output

   The BMPCC does not output sRGB by default.
   We will need to conimage it in :goto:`guides/bmpcc-hdmi-srgb`.

References
==========

.. [ColourScience-ACES12] https://github.com/colour-science/OpenColorIO-Configs/tree/feature/aces-1.2-config

.. [OpenColorIO-103] https://opencolorio.readthedocs.io/en/latest/configurations/aces_1.0.3.html
