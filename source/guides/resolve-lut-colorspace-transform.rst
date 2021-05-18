:author: |jake|
:author_url: |jake.url|
:date: 2021-05-18

=====================================
Generate a LUT Color Space Transforms
=====================================

.. guide:lesson::

    Generate a LUT from BlackmagicDesignFilmGen1 to sRGB or Linear sRGB.

.. note::

    The general concept described in this article can be applied to any camera.
    We like including reference implementations, since we have a BMPCC4K.

    If you would like to include another camera, please consider adding a guide!

The camera should be setup such that:

#. A maximum-quality Raw file is saved locally to SDCard, SSD, CFAST, etc.
#. A lower-quality (but the best you can make it) clean feed is sent to the Decklink for use with Composure.

Diagraming the physical components and color spaces, we get:

.. svgbob::
   :align: center

            Blackmagic    ┌────────┐
                Raw       │   SD   │
         ┌───────────────►│  Card  │
         │                └────────┘
         │
         │
    ┌────┴─────┐
    │          │
    │  Camera  │
    │          │
    └────┬─────┘
         │
         │
         │                 ┌─────────────┐            ┌──────────┐
         │     sRGB        │             │            │          │
         └────────────────►│ HDMI to SDI ├────SDI────►│ Decklink │
                           │             │            │          │
                           └─────────────┘            └──────────┘

The BMPCC4K records Blackmagic Raw files at 12-bit log,
under a variety of compression settings.

Documentation on Blackmagic color spaces is difficult at best.
[DaVinciResolve]_ can tell you your clips color space.
Our camera is set to [BlackmagicDesignFilmGen1]_ color space by default.

By default, the HDMI signal will use the same color space as our internal recording.
Unfortunately OCIO and Blackmagic do not play well together.
Specifically, OCIO does not have any input or output transforms for Blackmagic color spaces.

.. guide:next:: Alternative Approach Using OCIO

    An alternative would be to :goto:`guides/ocio-customize-add-blackmagic`.

We use a LUT to transform *only* the HDMI signal to a OCIO-friendly color space before sending to Unreal.
There are two good options from here:

#. Convert to sRGB
#. Convert to sRGB Linear

SRGB *looks right* when displayed on a monitor.
Linear sRGB is Unreal's working color space, and thus wouldn't require an input transform in composure.

In a very unscientific test, we processed an sRGB and linear sRGB test pattern through the 10-bit 4:2:0 sub-sampling used by our HDMI connection.

.. figure:: https://i.postimg.cc/X7cm2FF1/screenshot-45.png

    Linear sRGB (left) and sRGB (right) after converted to 10-bit and compressed in YCbCr using 4:2:0 chroma sub-sampling.
    Test pattern from [RTINGSChromaTest]_.

The sRGB linear appears to fair better in this example.
You can use either color space, as long as you understand the implications of both approaches.

Generating a LUT in Resolve
===========================

Our camera lets us apply a LUT before sending the image over HDMI.
We will use DaVinci Resolve to create a LUT which maps your cameras native color space to your preferred color space.
In our case, from BlackmagicDesignFilmGen1 to sRGBLinear.

#. Open Resolve and import any clip, an image, etc. It doesn't matter but we need a clip to "apply" our transforms to.

   .. figure:: https://i.postimg.cc/fyK400fP/screenshot-47.png
#. Go to the Color Grading tab, and in the Nodes library search for **Color Space Transform**

   .. figure:: https://i.postimg.cc/YqdKrY9G/screenshot-48.png
#. Add the transform to your node.

   .. figure:: https://i.postimg.cc/4yhDBSGr/recording.gif

#. Set your input and output color spaces accordingly.
   The input space is whatever your camera uses,
   and the output space is sRGB with appropriate gamma.
   Disable Tone Mapping, Forward OOTF, and Inverse OOTF.

   .. figure:: https://i.postimg.cc/CMGTB9vq/screenshot-49.png

   #. Gamma 2.2 is the sRGB default gamma.
   #. Gamma 2.4 is used by Rec.709.
   #. Linear is *Linear sRGB*.

#. With the color transform applied, right-click the clip and choose *Generate LUT*.
   The BMPCC4K uses a 33 point LUT.

   .. figure:: https://i.postimg.cc/X75ZCjRg/recording-1.gif

Save the file wherever you like.
It is now ready to be used as a color space transform in OCIO, your camera, or anywhere else!

.. guide:next:: Applying a LUT to the BMPCC4K

    Next, see :goto:`guides/bmpcc-hdmi-lut`.

References
==========

.. [BlackmagicDesignFilmGen1]

    .. figure:: https://i.postimg.cc/y6fS0ppL/screenshot-46.png

.. [DaVinciResolve]

.. [RTINGSChromaTest] 

    `<https://www.rtings.com/tv/learn/chroma-subsampling>`_
