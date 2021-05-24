:author: |jake|
:author_url: |jake.url|
:date: 21/05/2021

============================
sRGB vs sRGBLinear over HDMI
============================

When sending video from your camera to Unreal,
either via HDMI or SDI,
we believe that linear sRGB is the best color space to use.

.. admonition:: Learn the Theory

    See :doc:`/theory/colorspaces` to learn how color spaces work in detail.

Linear sRGB has the advantage of being Unreal's working space,
so your video does not need any OCIO color space mappings on import.
The downside is that any video displayed by your camera's LCD will look dark.
By contrast, SRGB *looks right* when displayed on a monitor,
but you will need to OCIO transform from sRGB to linear sRGB within Unreal.

In theory, either choice should be fine,
but there is one other matter that can affect the final image quality.

The [BMPCC4K]_'s HDMI port sends a 1080p 10-bit YCbCr 4:2:2 signal,
which uses chroma sub-sampling to use less bandwidth.
This means *less* data is being sent than if it were RGB, which is not sub-sampled.
Since our LUT converting to a known color space like sRGB is applied *before* the sub-sampling,
choosing the color space might have an affect on the quality of the image reaching Unreal.

.. svgbob::
    :align: center

                       ┌─────────────┐
                       │ Blackmagic  │       ┌───┐
                       │ Raw Encoder ├──────►│SSD│
                       └─────────────┘       └───┘
                         ▲
          ┌──────┐       │
    ─────►│ Raw  ├───────┤
          │ Data │       │
          └──────┘       ▼
                       ┌──────────────┐      ┌─────────────┐        ┌────────────┐
                       │BlackmagicFilm│      │HDMI YCbCr   ├───────►│Decklink 8K │
                       │ to sRGB LUT  ├─────►│4:2:2 Encoder│        └────────────┘
                       └──────────────┘      └─────────────┘

In a very unscientific test, we processed an sRGB and linear sRGB test pattern through the 10-bit 4:2:0 sub-sampling used by our HDMI connection.

.. figure:: https://i.postimg.cc/X7cm2FF1/screenshot-45.png

    Test pattern from [RTINGSChromaTest]_.

The sRGB linear appears to fair better in this example.
You can use either color space, as long as you understand the implications of both approaches.
