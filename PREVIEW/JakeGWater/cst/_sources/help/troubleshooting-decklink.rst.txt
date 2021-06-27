:author: |jake|
:author_url: |jake.url|

=====================================
Verifying the Decklink SDI Connection
=====================================

Verify your SDI connection with the Blackmagic MediaExpress app.

Blackmagic MediaExpress
=======================

#. Open Blackmagic MediaExpress.

   .. figure:: https://i.postimg.cc/Vvc4YQLp/image.png

#. Choose the decklink port your camera is connected to

   .. figure:: https://i.postimg.cc/GhZ3bdWq/image.png

#. Switch to the **Log and Capture** tab

   .. figure:: https://i.postimg.cc/QMKyhrrk/image.png

#. You should see your camera, live!

   .. figure:: https://i.postimg.cc/J7Qm9jx7/image.png

      Say hello to our head-model Bob.

#. Test your timecode by recording a short clip.

   .. figure:: https://i.postimg.cc/qR2GqJq0/image.png

   .. figure:: https://i.postimg.cc/gJbvfCD7/image.png

   The timecode won't show up until you play back the recorded clip.
   You should see the timecode from your camera appear under the *In* and *Out* labels.

   .. figure:: https://i.postimg.cc/LXhpFW8z/image.png

      Bob has never looked happier!

Troubleshooting
===============

.. list-table::
   :header-rows: 1
   :align: left
   :widths: 20 20 60

   * - Problem
     - Caused by
     - Fix
   * - The screen is black
     - No video input
     - Try another decklink port;
       Check all your wiring;
       Ensure you have setup your Decklink correctly in **Desktop Video Setup**.
   * - The video looks dark
     - Incorrect color space.
     - You might be outputting sRGB-linear or ACES instead of sRGB.
       Check the LUT being used by the camera.
   * - The video looks dull or washed out.
     - Incorrect color space.
     - You might be sending the Blackmagic Film color space over SDI.
       Unfortunately that color space is not in OCIO, and Unreal does not know how to convert it.
       Try enabling a Film-to-sRGB LUT on the HDMI signal.
   * - The device cannot be selected because it is greyed out.
     - Another application is using the video input.
     - Ensure Unreal or another app isn't using the SDI connection.
