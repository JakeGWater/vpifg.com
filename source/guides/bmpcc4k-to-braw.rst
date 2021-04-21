===============
BMPCC4k to BRaw
===============

.. topic:: Lesson Plan

    #. [BlackmagicRaw]_ vs [ProRes]_
    #. Camera Settings

.. planned::

Overview
========

We recommend recording to Blackmagic Raw because they work really well with Davinci Resolve.

Settings
========

* Record:

  * CODEC AND QUALITY:
  
    * **Blackmagic RAW**
    * **Constant Quality**
    * **Q0**
      The bit-rate of Constant Quality files varries, but BRaw Cosntant bitrate files with 3:1 compression use about 6 GB/minute according to [BRawDocs]_.
    
  * Resolution: Either of the following 
  
    * Choose **4K DCI** ``4096x2160`` if your intended output is *film*.
    * Choose **Ultra HD** ``3840x2160`` if your intended output is *TV*. This resolution matches the aspect ratio of 1080p, and will work a little better with your live preview.

  * Dynamic Range: **Film**. 
    You want to record at the largest dynamic range possible.

  * Project Frame Rate: 
  
    * Choose **24fps** if your intended output is *film*.
    * Choose **23.97** if your intended output is *TV*.

  * Apply LUT in File: **Off**

.. important::
    
    **Never Apply LUT In File** this will crush your dynamic range, and give you very little room to work with the footage in post.

* ISO

  * The BMPCC has two native ISOs.

    .. license:: FairUse
        :source: BlackmagicPocketCinemaCamera4KManual
        :source_url: https://documents.blackmagicdesign.com/UserManuals/BlackmagicPocketCinemaCamera4KManual.pdf

        When the ISO setting is between 100 and 1,000 the native ISO of 400 is used as a
        reference point. The ISO range between 1,250 and 25,600 uses the native ISO of
        3,200 as a reference. If you are shooting in conditions where you have a choice
        between ISO 1,000 or 1,250, we suggest closing down one stop on your lens’ iris so
        that you can select ISO 1,250 as it will engage the higher native ISO and provide much
        cleaner results.

    * We typically use 400 and leave it at that.

.. [BRawDocs] 
    
    https://documents.blackmagicdesign.com/UserManuals/BlackmagicPocketCinemaCamera4KManual.pdf

