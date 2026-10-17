# Game controllers, flight sticks, keypads and macro devices

Updated: 2026-10-17

What works on Steel OS, and how to set it up. "Works" means plugged in, with
no driver download. Entries marked **to test** are expected to work but have
not yet been tried on a Steel OS test PC.

---

## Gamepads

| Device | Status | Notes |
|---|---|---|
| Xbox One, Series X/S controllers (USB, Bluetooth) | Works | Built-in Linux driver |
| Xbox Wireless Adapter (the USB dongle) | Works | xone driver, included |
| PlayStation 4 and 5 controllers (USB, Bluetooth) | Works | Built-in Linux driver, including the touchpad and lights |
| Xbox and PlayStation clones (8BitDo, PowerA, GameSir and unbranded) | Works for most | Most present themselves as an Xbox controller. If one doesn't, Steam Input can still map it |
| Logitech F310 / F710 | Works | Use the **X** switch position (Xbox mode). D mode also works, as a generic gamepad |
| Nintendo Switch Pro controller | Works | Built-in Linux driver |
| GameCube controller adapter | Works | Driver included |

**In Steam:** Steam Input handles every gamepad above, including button
remapping per game. **Outside Steam:** most games read the controller
directly. For a game with no controller support, use **AntiMicroX** (Portal,
Gaming) to turn sticks and buttons into keys and mouse movement.

## Flight sticks, throttles and pedals

| Device | Status | Notes |
|---|---|---|
| Logitech / Saitek X52 and X52 Pro | Works (to test) | Every axis and button. The X52 Pro's small screen and lights need the separate x52pro tool, which isn't included |
| Logitech / Mad Catz X56 Rhino (stick and throttle) | Works (to test) | Appears as two devices, as on Windows |
| Thrustmaster T.16000M, TWCS throttle, T.Flight HOTAS, HOTAS Warthog | Works (to test) | |
| Logitech Extreme 3D Pro | Works | |
| VKB, Virpil, Leo Bodnar-based controls | Works (to test) | |
| Rudder pedals (Thrustmaster, Saitek, MFG) | Works (to test) | |

Steel OS lets games running through Proton or Wine (Star Citizen, Elite
Dangerous, DCS and Microsoft Flight Simulator among them) read these devices
directly, as they do on Windows. Test any of them in Portal, Gaming, **Test a
controller or flight stick**.

## Racing wheels

| Device | Status | Notes |
|---|---|---|
| Logitech G29, G920, G923 and older | Works | Force feedback included (new-lg4ff driver) |
| Thrustmaster T300, T150, TMX, T248, TX | Works (to test) | Force feedback drivers included |
| Fanatec wheels and bases | Works (to test) | Driver included |

**Oversteer** (Steel Apps) sets rotation, force-feedback strength and buttons.

## Gaming keypads, keyboards and mice with macros

| Device | Status | How to set it up |
|---|---|---|
| Razer Tartarus V2 (and Pro), Orbweaver | Works as a keypad; lights and key maps after installing Razer support | Portal, Gaming, **Razer devices**, then Polychromatic. Macros: Input Remapper |
| Belkin / Razer Nostromo N52, N52te | Works as a keypad | Macros and key maps: Input Remapper |
| Razer keyboards and mice | Work; lights and DPI after installing Razer support | Polychromatic |
| Logitech G mice and keyboards | Work | Buttons, DPI and lights: **Piper**. Wireless: **Solaar** |
| SteelSeries, Roccat and other gaming mice | Work; many supported by Piper | Piper |
| Any keyboard, mouse or keypad | Works | **Input Remapper** records macros and remaps any key or button, per device |

**Macros:** Portal, Gaming, **Macros for keyboards, mice, keypads and
controllers** opens Input Remapper. Pick the device, press the key to change,
and type what it should do: another key, a key combination, or a macro such as
`key(1).wait(100).key(2)`. Saved settings load at every login.

## How to report a device that doesn't work

At steel-os.org/report, give the device's name, how it's connected (USB,
Bluetooth or dongle), what doesn't work, and the output of this command:

```
lsusb
```
