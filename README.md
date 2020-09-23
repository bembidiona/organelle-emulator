# MOM
a Mother with oled screen and multipage support. Or simply put: An Organele emulator! :)\
Also check my other organelle's patches [here](https://github.com/bembidiona/organelle-patches)


<p align="center">
  <img width="90%" src="https://raw.githubusercontent.com/bembidiona/organelle-emulator/master/_readme/mom_banner.jpg">
</p>
Graphic test on various patches:
<p align="center">
  <img width="24%" src="https://raw.githubusercontent.com/bembidiona/organelle-emulator/master/_readme/gif_drawave.gif">
  <img width="24%" src="https://raw.githubusercontent.com/bembidiona/organelle-emulator/master/_readme/gif_pianelle.gif">
  <img width="24%" src="https://raw.githubusercontent.com/bembidiona/organelle-emulator/master/_readme/gif_roll.gif">
  <img width="24%" src="https://raw.githubusercontent.com/bembidiona/organelle-emulator/master/_readme/gif_poke.gif">
</p>



## FEATURES:
- Pretty accurate representation of the organelle screen. There is support for /oled/gFlip /oled/gClear /oled/gSetPixel /oled/gLine /oled/gBox /oled/gFillArea /oled/gCircle /oled/gFilledCircle /oled/gPrintln /oled/gInvertArea /oled/gInvertLine /oled/gShowInfoBar, screenLines and a bunch of other calls.
- Support of the note buttons, aux, encoder, vol, foot pedal, knobs, led light, etc. All mapped to keyboard keys.
- It’s tiny and cute :)

### How to launch the SCREEN
The emulated screen is made with pygame. To launch it you will need to do one of these:
- A – If you are on Windows just run oled.exe and that’s it.
- B – If you are not on Windows, or you don’t want to run a executable, you will need to have installed Python 3, and the pygame and python-osc modules. Once you have installed all this, just run oled.py.
The OLED toglebox on MOM.pd is for updating/restarting the screen. Be sure to have it checked.

#### UPDATE 1.1:
- Change the name to something less e d g y
- Added a .exe for those people in windows that don’t want to install python.
- Now there is support for multipage patches! I test it with Zone and Jeraphy and they run fine.
Keep in mind that to be able to run these patches on desktop, you should disable their versioncheck object! To do this, just bypass it, and connect [loadbang] directly to the [t b b] object.

#### UPDATE 1.2:
- OLED Window’s size can be set from the script.
- Added a panic button.
- Fix bugs in the encoder. Now it send the correct calls.
- Added a reboot button for the Oled.
- Added expression pedal.
