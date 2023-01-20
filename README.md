# Overkill PIU Pad Lighting Kit
An upgrade kit, if you consider a 5x5 RGB LED matrix in the center of each panel to be an upgrade.

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

This project is compatible with:
* Pump it Up FX, CX, TX, and LX
* Some older pads (SX and prior) may require some cable splicing or custom adapters. Try at your own risk!

Without some modification, this project is **NOT** made to be compatible with:
* Dance Dance Revolution machines
* StepManiaX machines
* Anything that's not Pump it Up, really

Aside from the individual components required for each PCB, you will need:
* As many "Panel" PCBs as your upgrade requires, likely 5 or 10 total depending on whether you're upgrading 1 or 2 full pads
* A power supply that can provide up to ~15A maximum current at 5 volts (75W or so)
    * This can be either one 7.5-8A power supply **per pad**, or one single super beefy power supply for **both pads simultaneously.**
* Extra wiring to supply power to the new PCBs

# Credits
Thanks to:
- [sugoku](https://github.com/sugoku) for the Molex 35312 series footprints
