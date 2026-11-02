# Heltec WiFi LoRa 32 V3

Hardware package for the ESP32-S3 board with 8 MB flash, SX1262 radio, 128×64
SSD1306 OLED, PRG button, and GPIO35 LED. The demo requires ESPHome 2026.9.1 or
newer for early OLED power-supply initialization.

See the root README for [package usage](../../README.md#usage),
[running demos](../../README.md#trying-out-the-demos), and
[development commands](../../CONTRIBUTING.md).

## Hardware notes

`lora_radio` identifies the SX1262 and `led` the onboard white LED. `oled_power`
controls the active-low Vext rail on GPIO36; the OLED and header Vext supply
share that rail. Applications using the OLED must power it before I2C recovery.
The [demo](demo.yaml) extends `oled_power` with `enable_on_boot: true` and
`enable_time: 20ms`; the board package leaves startup policy to the application.
The OLED uses SDA17/SCL18, reset21, address 0x3C.
The radio uses SCK9/MOSI10/MISO11, CS8/reset12/BUSY13/DIO1 14, DIO2 RF switching,
and a 1.8 V TCXO. PRG is active-low GPIO0.

`battery_voltage` samples GPIO1/ADC1 through the onboard 390k/100k divider;
the calibrated ADC voltage is multiplied by 4.9. `battery_adc_enable` controls
the divider gate on GPIO37. It defaults to active-low per the earlier schematic
and is off initially when that polarity matches the hardware. The sensor does not poll automatically: the application must
enable the gate, allow settling, update the sensor, then disable the gate.
The demo performs that sequence every 30 seconds with a nonblocking 10 ms delay
and eight ADC samples. The first sample runs after component startup.

Board revisions can reverse the GPIO37 polarity (Heltec's V3.2 example uses
active-high, whereas the earlier schematic uses active-low). The official MeshCore
board adapter detects the inactive pull level at startup; this declarative
package instead makes the polarity explicit. For a board with an active-high
gate, override only the existing output pin polarity:

```yaml
output:
  - id: !extend battery_adc_enable
    pin:
      inverted: false
```

This is battery-terminal voltage, not a fuel gauge or charge-status signal.
The charger may produce a plausible voltage even without a battery, and voltage
under load or while charging is not an accurate remaining-capacity measurement.
Check polarity and voltage against the actual board/battery before relying on it.

## Demo

The [demo](demo.yaml) displays raw received-packet count, RSSI/SNR and battery
voltage. PRG toggles the onboard LED. It uses a receive-only 910.525 MHz / 62.5 kHz / SF7 / CR4/5 profile;
change the profile to match your local devices and board frequency band. It does
not transmit or implement MeshCore, Meshtastic, or LoRaWAN.

UART0 logs use the board's USB-UART connection at 115200 baud.

## Verification and sources

On 2026-11-01, lint, configuration validation and compilation passed with ESPHome
2026.9.1 / ESP-IDF 5.5.5 (300791-byte image). The review revision also passes
ESPHome 2026.10.1 / ESP-IDF 5.5.6 (299371-byte image); moving startup settings
into the demo leaves its merged configuration unchanged. The extracted
radio/OLED/power wiring was previously exercised on a physical V3 during a
separate ESPHome MeshCore prototype.

The standalone demo from revision `88d0205` was flashed on 2026-11-01. Serial
logs confirm successful startup, active Vext, SSD1306 I2C initialization and the
SX1262 radio profile without setup errors. The device partition table matched;
NVS remained byte-for-byte unchanged after flashing and after boot. Previous
room identities and history were preserved in storage, though this demo does not
run room services. The user confirmed the OLED display and PRG button toggling
the white LED. Received-packet activity on this demo remains unconfirmed.
Battery measurement was added subsequently; charge status is not exposed.
On 2026-11-01 the battery update passed board YAML lint, demo configuration and
an additional consumer that extends the gate/sensor and adds another sensor.
The updated demo compiles with ESPHome 2026.10.1 / ESP-IDF 5.5.6 at 313283 bytes
flash and 56791 bytes static RAM. This demo revision was not flashed.

The battery hardware was exercised by the separate MeshCore V3 application on
the connected board with a user-confirmed single-cell LiPo. Active-low gating
returned 0.16 V; the documented active-high override returned 4.14 V. The gate
is enabled only during each sampling sequence. These readings verify operation
on that board, not meter calibration, charge status or every V3 revision.

Sources checked 2026-11-01:

- [Heltec V3.2 schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V3/WiFi_LoRa_32_V3.2_Schematic_Diagram.pdf)
- [Heltec V3.2 datasheet](https://resource.heltec.cn/download/WiFi_LoRa_32_V3/HTIT-WB32LA_V3.2.pdf)
- [Arduino-ESP32 3.3.1 V3 pin map](https://github.com/espressif/arduino-esp32/blob/3.3.1/variants/heltec_wifi_lora_32_V3/pins_arduino.h)
- [ESPHome SX126x component](https://esphome.io/components/sx126x/)
- [MeshCore V3 ADC gate polarity handling](https://github.com/meshcore-dev/MeshCore/blob/81dbae592ffad40b4212bc0b37e82b38da08f4bc/variants/heltec_v3/HeltecV3Board.h)
- [ESPHome calibrated ADC sensor](https://esphome.io/components/sensor/adc/)
- [Heltec V3.2 battery reading example](https://github.com/HelTecAutomation/Heltec_ESP32/blob/master/examples/ESP32/WiFiLoRa32_battery_read/WiFiLoRa32_battery_read.ino)
