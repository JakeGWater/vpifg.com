:author: |jake|
:author_url: |jake.url|
:date: 2021-05-18

=====================================
Generate a LUT Color Space Transforms
=====================================

.. guide:lesson::

    Generate a LUT from Blackmagic's Custom Color Space to sRGB or Linear sRGB.

.. note::

    The general concept described in this article can be applied to any camera.
    We include the reference implementations using a BMPCC4K.

    If you would like to include another camera, please consider adding a guide!

The [BMPCC4K]_ records Blackmagic Raw files in a custom wide-gamut color space.
By default, the camera's HDMI video feed will use the same color space as its internal recording.
Our camera uses [BlackmagicDesignFilmGen1]_. 

.. sidebar:: Color Space as Language

    Imagine our camera speaks French, but Unreal expects English.
    Somewhere, we need a translator.
    In this example, the camera will translate to English before speaking to Unreal.

Unfortunately Unreal does not know anything about this color space,
meaning the footage will look incorrect.
It will either be too dark, or washed out.

OCIO is a tool used by Unreal to convert between color spaces,
but it also doesn't know the BlackmagicDesignFilmGen1 color space.
What we should do is tell the camera to send a color space that Unreal recognizes.
In this case, sRGB Linear.

.. rubric:: Our Objective

#. A 4K :term:`Raw` file is saved to your camera's removable media cards, such as an SDCard, USB-C hard drive, or CFAST card.
   The Raw file will use a wide-gamut color space, and preserve as much image data as possible.
#. A 1080p clean feed is sent to the Decklink via HDMI/SDI for use with Unreal's Composure tool.
   The HDMI feed uses the sRGB linear color space, which matches Unreal. 

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

To send sRGB linear from the camera,
we apply a LUT specially generated to transform video from BlackmagicDesignFilmGen1 to sRGB Linear.
We have to manually create the LUT, but it can be generated using DaVinciResolve.

By default, the HDMI signal will use the same color space as the camera's internal recording,
which in our case is BlackmagicDesignFilmGen1.
Unfortunately OCIO and Blackmagic do not play well together.
Specifically, OCIO does not have any input or output transforms for Blackmagic color spaces.

.. guide:next:: Alternative Approach Using OCIO

    An alternative would be to :goto:`guides/ocio-customize-add-blackmagic`.

We use a LUT to transform *only* the HDMI signal to an OCIO-friendly color space before sending to Unreal.
The Raw file recorded internally to the camera should not be affected.

We recommend use sRGB linear over HDMI/SDI, because that is the default color space used by Unreal.
It is possible to use another color space, but we will reference using sRGB linear in the following examples.

.. admonition:: sRGB vs sRGB Linear Deep Dive

    See our comparison of :goto:`help/sRGB-or-sRGB-linear`.

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
   and the output space is sRGB with appropriate gamma:
   
   #. Gamma 2.2 is the sRGB default gamma used by computer monitors.
   #. Gamma 2.4 is used by Rec.709 which is for HDTV.
   #. Linear is best when importing to another VFX program, including Unreal, and Nuke.

   Also disable Tone Mapping, Forward OOTF, and Inverse OOTF.

   .. figure:: https://i.postimg.cc/CMGTB9vq/screenshot-49.png

.. admonition:: How Do I Find My Camera's Color Space?

    See :goto:`help/find-my-color-space` if you're unsure which input space to use.

#. With the color transform applied, right-click the clip and choose *Generate LUT*.
   The BMPCC4K uses a 33 point LUT.

   .. figure:: https://i.postimg.cc/X75ZCjRg/recording-1.gif

Save the file wherever you like.
It is now ready to be used as a color space transform in your camera, or anywhere else!

.. guide:next:: Applying a LUT to the BMPCC4K

    Next, see :goto:`guides/bmpcc-hdmi-lut`.

