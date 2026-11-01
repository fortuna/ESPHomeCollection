# Heltec WiFi LoRa 32 V3

Hardware package for the ESP32-S3 board with 8 MB flash, SX1262 radio, 128×64
SSD1306 OLED, PRG button, and GPIO35 LED. It requires ESPHome 2026.9.1 or newer
for the early power-supply initialization used by the OLED rail.

```yaml
packages:
  board: !include board.yaml
```

Include this package from your device configuration. It contains hardware only;
add your logger, network/radio profile, fonts, display content and button actions
in that configuration. Extend `oled_display` and `boot_button` with `!extend`.
`lora_radio` identifies the SX1262 and `led` the onboard white LED. `oled_power`
drives the active-low Vext rail on GPIO36 before I2C recovery; the header Vext
supply shares that rail. The OLED uses SDA17/SCL18, reset21, address 0x3C.
The radio uses SCK9/MOSI10/MISO11, CS8/reset12/BUSY13/DIO1 14, DIO2 RF switching,
and a 1.8 V TCXO. PRG is active-low GPIO0.

## Demo

The demo displays raw received-packet count and RSSI/SNR, and PRG toggles the
onboard LED. It uses a receive-only 910.525 MHz / 62.5 kHz / SF7 / CR4/5 profile;
change the profile to match your local devices and board frequency band. It does
not transmit or implement MeshCore, Meshtastic, or LoRaWAN. No Wi-Fi, API, OTA,
secrets, external components, or adjacent repository files are required.

```sh
yamllint boards/heltec-wifi-lora-32-v3
esphome config boards/heltec-wifi-lora-32-v3/demo.yaml
esphome compile boards/heltec-wifi-lora-32-v3/demo.yaml
```

Run commands from the repository root. The first build downloads the font and
toolchain. Uploading the demo replaces the installed firmware; preserve existing
firmware/state first. UART0 logs use the board's USB-UART connection at 115200 baud.

## Verification and sources

On 2026-11-01, lint, configuration validation and compilation passed with ESPHome
2026.9.1 / ESP-IDF 5.5.5. Image size: 300791 bytes. The extracted radio/OLED/power
wiring was previously exercised on a physical V3 during a separate ESPHome
MeshCore prototype. This standalone demo and the GPIO35 LED interaction have not
been flashed/tested; compilation is the acceptance evidence for this PR.
Battery measurement/charge status are not exposed by this package.

Sources checked 2026-11-01:

- [Heltec V3.2 schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V3/WiFi_LoRa_32_V3.2_Schematic_Diagram.pdf)
- [Heltec V3.2 datasheet](https://resource.heltec.cn/download/WiFi_LoRa_32_V3/HTIT-WB32LA_V3.2.pdf)
- [Arduino-ESP32 3.3.1 V3 pin map](https://github.com/espressif/arduino-esp32/blob/3.3.1/variants/heltec_wifi_lora_32_V3/pins_arduino.h)
- [ESPHome SX126x component](https://esphome.io/components/sx126x/)
