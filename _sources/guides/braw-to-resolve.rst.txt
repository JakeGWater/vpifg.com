########################
BRaw to Davinci Resolve
########################

.. wip::

First, ensure your Blackmagic camera is set to correctly record BRaw.
See :doc:`bmpcc4k-to-braw`.

.. note:: We are using Davinvi Resolved 17.

Project Setup
=============

In your project settings:

#. Under *Color Management* select the *ACEScc* or *ACEScct* color space. This will insure your project timeline color space is ACES, and when importing and combining footage from other sources it will be possible to maintain your Color Pipeline.
#. While importing, editing, or color grading you should set your *Output Display Transform* to match your display gamut. If you are unsure, choose between sRGB or Rec.709.

.. warning::
    When exporting from Resolve, you **must remove** your *Output Display Transform*. Otherwise your exported footage will be comprssed to your *smaller* display color space. See :doc:`resolve-to-nuke` for more details.

Timecode Integrity
------------------

BlackmagicRaw files have timecode embedded in them, and Davinci Resolve will automatically read the time code from those files.

Color Pipeline
--------------

Resolve knows which color spaces your BRaw files were recorded in. 
When working in ACES, you do not need to set any input transforms as Resolve will correctly apply them when importing.
