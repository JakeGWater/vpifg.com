##################
Timecode Integrity
##################

.. wip::

Timecode integrity will make our lives easier at every step.
Even for a short film, there may be hundreds of shots, each requiring post-production and vfx.

Youw will encounter multiple types of timecode encodings.

.. glossary::

    SMPTE
        Is a timecode encoding embedded into your HDMI or SDI signal.

        Example: ``01:04:29:16``
    
    VITC
        Vertical interval timecode embeds an SMPTE-encoded timecode between every frame.
        Cameras that *output timecode* probably use this.

        The [BMPCC4k]_ outputs VITC over HDMI.
    
    LTC
        Linear timecode embeds an SMPTE timecode into an audio channel.
    
    Frame Number
        Typically used in formats like EXR, where there is one file per frame. 
        Each file is enumerated monotonically counting upward from the stating frame.

        Example: ``scene1-shot3-00014291.exr``

        [Nuke]_ natively uses Frame Numbering. [Resolve]_ can use both Frame Numbering as well as SMPTE timecodes.
