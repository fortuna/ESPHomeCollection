# Heltec Mesh Node T096 — experimental GPIO bring-up

**Draft, not a complete ESPHome T096 port.** The board uses an nRF52840, not an
ESP32. This package models its LED, user button and peripheral-control GPIOs.
The demo toggles the white LED when the button is pressed and logs over USB CDC.
LoRa, TFT, GNSS, battery measurement and MeshCore services are not implemented.

## Build profile and bootloader

ESPHome has no native T096 board definition. This draft uses its documented
`adafruit_itsybitsy_nrf52840` compatibility profile for the same MCU, with an
explicit `adafruit_nrf52_sd140_v6` layout. That layout reserves 0x00000–0x25fff
for the SoftDevice and 0xf4000–0xfffff for the bootloader. The selection follows
MeshCore's pinned T096 linker configuration; it is **not confirmation of the
bootloader installed on a particular T096**. Check the actual bootloader and
preserve firmware/state before considering a flash. Do not replace the bootloader
or erase UICR based on this draft. DC/DC is explicitly disabled for initial bring-up.

The local `heltec_t096_platform` helper removes inherited ItsyBitsy QSPI flash,
SPI/I2C/UART/ADC/802.15.4 peripherals and LED/button aliases. In particular, the
ItsyBitsy QSPI driver would drive pins used by the T096 radio, so the helper is
required even for this GPIO-only demo. It adds no runtime driver or application
behavior; actual T096 GPIO definitions remain in `board.yaml`.

Clone the repository and keep the helper alongside this board package. A config
outside this directory must override `t096_components_path` with the relative
path to `boards/heltec-mesh-node-t096/components` from that config. A remote
`github://` board-only import is not supported by this draft's local helper.

No physical T096 has been flashed with this configuration. Before promoting this
PR from draft, verify the resulting devicetree, bootloader
layout, USB, GPIO polarity and initial rail levels on the actual board, or replace
it with a native T096 Zephyr board definition.

## Hardware definitions

All modeled hardware is in `board.yaml`; the application behavior is in `demo.yaml`.
The outputs start logically off, including the active-low GNSS and backlight
controls. The demo never enables these peripheral outputs. Their initialization
levels have source/code inspection, not physical measurements.

| Function | MCU pin(s) | Current package |
| --- | --- | --- |
| White LED | P0.28, active high | `led` / `led_output` |
| User button | P1.10, active low | `boot_button`, pull-up |
| Vext/display rail | P0.26, active high | `peripheral_power`, off |
| GNSS power | P0.06, active low | `gnss_power`, off |
| TFT backlight | P1.12, active low | `display_backlight`, off |
| FEM rail / CSD / CTX | P0.30 / P0.12 / P1.09 | `fem_power`, `fem_enable`, `fem_path_select`, off |
| Battery-divider enable | P1.15, active high | `battery_adc_enable`, off |
| LoRa SPI SCK/MOSI/MISO | P1.08 / P0.11 / P0.14 | Not enabled |
| LoRa CS/reset/BUSY/DIO1 | P0.05 / P0.16 / P0.19 / P0.21 | Not enabled |
| LoRa RF switch / TCXO | SX1262 DIO2 / DIO3, 1.8 V | Not enabled |
| TFT SCK/MOSI/CS/DC/reset | P0.20 / P0.17 / P0.22 / P0.15 / P0.13 | Not enabled |
| GNSS MCU RX/TX/reset/PPS | P0.23 / P0.25 / P1.14 / P1.11 | Not enabled |
| Battery ADC | P0.03 / AIN1 | Not enabled |
| Exposed I2C pairs | P0.07/P0.08 and P0.04/P0.27 | Not configured |

The KCT8103L front end needs coordinated rail, CSD, CTX and SX1262 DIO2 handling.
A plain SX1262 setup is insufficient, and chip TX power is not antenna output
power. These GPIO outputs are groundwork, not a radio-control driver.

## Platform gaps

ESPHome 2026.10.1's ordinary SPI component still lists ESP32, ESP8266 and RP2
platforms, excluding nRF52. Therefore the stock SX126x and SPI TFT components
cannot be composed into this board package yet. Native nRF52 SPI support plus
FEM sequencing and display initialization are prerequisites for those peripherals.
GNSS/ADC and their power sequencing also need separate validation. This draft
intentionally avoids nonfunctional `sx126x`/display declarations.

The board package does not satisfy the ESP32/ESP-IDF requirement of the separate
esphome-meshcore prototype. That project needs nRF52 platform adapters too.

## Validation

Commands from the repository root:

```sh
yamllint boards/heltec-mesh-node-t096
esphome config boards/heltec-mesh-node-t096/demo.yaml
esphome compile boards/heltec-mesh-node-t096/demo.yaml
```

Configuration, repository YAML lint, and compilation pass with ESPHome 2026.9.1
and the native sdk-nrf toolchain / nRF Connect SDK 2.9.2. The generated UF2 starts
at 0x26000. Build inspection confirms that QSPI, SPI, I2C and ADC drivers are not
active, the inherited peripheral nodes are disabled, and UICR writes/pin-reset
configuration are disabled. This is build evidence only; no hardware acceptance
has been performed.

## Sources checked 2026-11-01

- [Heltec T096 product and MCU](https://heltec.org/project/t096/)
- [Heltec T096 datasheet, pin tables pp. 6–8](https://resource.heltec.cn/download/Mesh_Node_T096/Datasheet/Mesh%20Node%20T096.pdf)
- [Heltec T096 schematic V0.2](https://resource.heltec.cn/download/Mesh_Node_T096/Schematic/Mesh_Node_T096_V0.2.pdf)
- [MeshCore v1.18.0 T096 pin map](https://github.com/meshcore-dev/MeshCore/blob/81dbae592ffad40b4212bc0b37e82b38da08f4bc/variants/heltec_t096/variant.h)
- [MeshCore T096 bootloader/FEM/GNSS settings](https://github.com/meshcore-dev/MeshCore/blob/81dbae592ffad40b4212bc0b37e82b38da08f4bc/variants/heltec_t096/platformio.ini)
- [ZephCore T096 board reference](https://github.com/liquidraver/ZephCore/blob/d2f65687efd5bfd7dfef7d521cbe74469f17ff64/zephcore/boards/nrf52840/heltec_t096/README.md)
- [ESPHome nRF52 and compatibility profiles](https://esphome.io/components/nrf52/)
- [ESPHome 2026.10.1 SPI platform support](https://github.com/esphome/esphome/blob/2026.10.1/esphome/components/spi/__init__.py)
- [ESPHome 2026.9.1 nRF52 bootloader regions](https://github.com/esphome/esphome/blob/2026.9.1/esphome/components/nrf52/boards.py)
