============
Production
============

While independent productions are our focus,
our aim is towards professional content that is sellable.
Thus we aim to ensure all guides and workflows are :term:`Production Ready`.

.. glossary::

    Production Ready
        Production Ready content should meet broadcast standards, and for lack of a better term be *sellable*. 
        More simply, production ready content must maintain its :doc:`/production/color/pipeline` and preserve :doc:`/production/timecode`.

Exactly what makes something production ready depends on the production.
Therefore we score every workflow against the following checklist.

Production Checklist
====================

.. toctree::
    :glob:
    :hidden:

    production/*

We score workflows against the following elements.

.. glossary::

    Timecode
        Timecode requires for projcts with post-production, that all hardware and software that consumes or produces media to maintain the original timecode both on import and export.
        
        See more in :doc:`/production/timecode`.

    ACES
        ACES is the prefered color pipeline. ACES requires that Raw files are exported only to ACES, and not another smaller color space.
        Correct input and output transforms must be used to maintainer your color pipeline.
        CG footage may be exported to ACEScg.

        See more in :doc:`/production/color`.
    
    4K
        We believe 4K source and output files are the minimum requirment for selling content, even if eventually downsampled.

    Raw
        Raw requires that all original footage is shot in that cameras RAW format. 
        Footage should not be re-encoded to a colorspace outside of ACES. 

    Live
        Live requires the ability to output a Rec.709/sRGB or wider-gamut 1080p or better video signal.

    Multicam
        Multicam requires that for multiple cameras, they are genlocked if shooting live or with nDisplay.

    nDisplay
        nDisplay requires that all input sources are genlocked, and that same synchronization signal is driving the nDisplay wall.
