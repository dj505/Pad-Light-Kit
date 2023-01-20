# Overkill PIU Pad Lighting Kit
An upgrade kit, if you consider a 5x5 RGB LED matrix in the center of each panel to be an upgrade.  

![Render](Panel/Images/Render.png)

# What is this?
I wanted to make a drop-in kit that replaced the original LEDs in Pump it Up dance pads with fancy StepManiaX-like RGB lighting. **This is only partially that.** Due to a variety of factors, it's not quite as drop-in as I'd hoped.

There are 2 PCB designs being worked on for this project:
* The main "Panel" PCB
    * Contains all the LEDs, with individual microcontrollers per PCB, ensuring they can all work individually.
    * Complete, but untested. Check back in a month or two!
* The power distrubution PCB
    * Still a work in progress, not yet complete, maybe entirely unnecessary. We'll see.

Unlike the PicoFX and my other previous hardware projects, this kit is not meant to be hand-soldered, although hand-solder friendly footprints were used where possible. Please keep in mind the PCB manufacturing and assembly costs for this project may be rather high. As this likely will not be sold as a pre-made kit any time soon, be aware that it is not a beginner project.

# Compatibility & Overview

### This project is designed to be as easy as possible to install, but does require you to do some amount of manual part sourcing. Please pay close attention to power consumption and make sure you source parts that can support the kit.

This project is made for somewhat modern Pump it Up dance pads (FX through LX), but is also plug-and-play compatible with:
* All Pump it Up dance pads **after** SD (SD pads used incandescent bulbs. Please don't wire 120/240V to the 12V input)
* In the Groove pads
* Older Dance Dance Revolution pads that use the same 2.54mm pitch connector (double check first!)
Please **pay close attention to the polarity** of the 12V connector printed on the PCB's silkscreen.  
The **yellow wire should go to 12V.** This may involve plugging the cable in upside down. That's okay.

Without some modification to the pads and/or this kit, this project is **NOT** plug-and-play compatible with:
* Pump it Up JUMP pads (unfortunate, I know)
* Modern Dance Dance Revolution pads
* Namco "Crapocab" DDR pads
* StepManiaX pads (for several reasons)
* Dance Master Super Station/3DDX
* EZ2Dancer
If the pads you want to use this project with have a **12V DC** wire that powers the original lights, whether it goes to existing LEDs or to an inverter, **this kit will function, but may require you to cut the wires and/or splice in a new connector.** It likely will also not fit the original mounting holes, in which case you'll need to tape it down or something.

Aside from the individual components required for each PCB, you will need:
* As many "Panel" PCBs as your upgrade requires
    * PIU pads require 5 per full pad
    * ITG/DDR pads require 4 per full pad
* A power supply that can provide up to ~15A maximum current at 5 volts (75W or so)
    * This can be either one 7.5-8A power supply **per pad**, or one single super beefy power supply for **both pads simultaneously.**
    * If I did my math right, these metrics are based on the peak power comsumption when every single LED is lit up white at full brightness. **Only your LEDs on full-brightness white for extended periods of time at your own risk; the kit was not developed with this use in mind.**
* Extra wiring to supply power to the new PCBs

# Bill of Materials
A full BOM can be found in the "Assembly" folder. Unlike my previous projects, such as the PicoFX or PicoIO, there are a *lot* of components that you will likely need to source yourself. Many of these have LCSC part numbers attached as an example, but are not guaranteed to be available through JLCPCB's assembly service.  
The following components (some of which are not required) are listed per **1** PCB:

|          Component          |          Footprint         |Quantity|
|-----------------------------|----------------------------|--------|
|100nF Capacitor              |SMD 0402                    |10      |
|1uF Capacitor                |SMD 0402                    |2       |
|27pF Capacitor               |SMD 0402                    |2       |
|10uF Capacitor               |SMD 0402                    |2       |
|WS2812B LED                  |PLCC4 5x5mm                 |25      |
|1N4001 Diode \*              |THT                         |1       |
|3 Pin Header \*              |2.54mm Pitch                |1       |
|USB Type C Port              |GCT USB4085                 |1       |
|2 Pin JST XH                 |2.50mm Pitch                |1       |
|2x6 Pin Header \*            |2.54mm Pitch                |1       |
|Molex 35312-0760 \~\~        |N/A                         |1       |
|Molex Mini-Fit Jr \~\~       |N/A                         |4       |
|2 Pin Header \~              |2.54mm Pitch, **Horizontal**|1       |
|3 Pin Header \*\*            |1.27mm Pitch, Not Required  |2       |
|10k Ohm Resistor             |SMD 0402                    |1       |
|10K Ohm Resistor \*\*        |SMD 0402 (for SPI flash)    |1       |
|27 Ohm Resistor              |SMD 0402                    |2       |
|5.1k Ohm Resistor            |SMD 0402                    |2       |
|3k Ohm Resistor              |SMD 0402                    |1       |
|1k Ohm Reistor               |SMD 0402                    |3       |
|Tactile Button Switch        |6mm x 6mm                   |2       |
|W25Q32JVSS (or equivalent)   |SOIC-8                      |1       |
|Raspberry Pi RP2040          |QFN-56                      |1       |
|NCP1117 3.3V Output Regulator|SOT-223-3                   |1       |
|12.000MHz Crystal Oscillator |HC49                        |1       |

\* Optional  
\*\* Do Not Fit (only required if a part malfunctions without it)  
\~ Required for old-style pads (FX and earlier)  
\~\~ Required for new-style pads (CX/TX and newer)  

All **SMD 0402** parts use hand-solder footprints in just in case, however if you do not own a reflow oven or hot air soldering station, please consider using an assembly service available through companies like PCBWay or JLCPCB for a better and more realiable end result. It does cost extra, but will be far less time consuming and far more reliable than soldering hundreds of components by hand.

# Very Important Notes
### This kit will require a dedicated power supply and there's no safe way around that.
I'm not an electrician and I don't have a strong grasp of the fine details involved in power management, but I do know that it's not safe to run too much current through a wire that can't handle it.
Please don't try to power this off the cab's original 12V line! The original 22AWG wire is rated for roughly 0.92A. This kit can potentially draw over 1.5A per panel, or over 7.5A total per pad.  
Make sure you use a power supply that's capable of supplying the necessary amount of power required by this kit, and pick a wire gauge capable of carrying the amount of power needed for each panel. 20AWG is recommended at minimum.  
You'll likely end up with 1-2 extra power supply cables running through the bottom your pads. If I can come up with a more elegant solution I'll be sure to post it in detail.  
**Make sure you use a bright solder mask!!!** White is recommended, green and others may also work, but black solder mask isn't known to be very reflective.

# Credits
Thanks to:
- [sugoku](https://github.com/sugoku) for the Molex 35312 series footprints
