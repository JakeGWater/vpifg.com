============
Theory
============

.. toctree::
    :glob:
    :hidden:
    
    theory/*

We believe the following topics are important to Virtual Production,
and each workflow is evaluated using the following *Production Checklist*.

.. glossary::

    Timecode
        Timecode requires that all hardware and software that consumes or produces media to maintain the original timecode both on import and export.
        
        See more in :doc:`/theory/timecode`.

    ACES
        ACES requires an ACES working space and that Raw files are exported only to ACES, and not another smaller color space.
        Correct input and output transforms must be used to maintainer your color pipeline.
        CG footage may be exported to ACEScg.

        See more in :doc:`/theory/aces`.
    
    4K
        4K requires that all sources, both camera an renders, are either 3840x2160 or 4096x2160 resolution,
        and those sources are not downsabled to a smaller solution during processing.

    Raw
        Raw requires that all original footage is shot in that cameras RAW format at 10-bit color depth or higher,
        and written using a relatively high-quality compression and color-space.
        Raw footage should only be re-encoded in a lossless format to-and-from ACES.

    Live
        Live requires the ability to output a Rec.709/sRGB or wider-gamut 1080p or better video signal in real time.

    Multicam
        Multicam requires that for multiple cameras, they are genlocked if shooting live or with nDisplay.

    nDisplay
        nDisplay requires that all input sources are genlocked, and that same synchronization signal is driving the nDisplay wall.

.. admonition:: Use Your Judgement

    Perfect is the enemy of done.
    We want to keep people walking down the right path,
    but don't want that path so narrow nothing gets done.
    
    The Production Checklist is an attempt to objectively compare workflows,
    it is not a guaruntee of success nor is lack of a checklist item an indication of a bad workflow.
