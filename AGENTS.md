# Repository guidance

Read [README.md](README.md) for the repository layout, board/demo conventions,
development commands, and contribution process. Keep board-specific capabilities,
source references, and verification limits in the board's README.

## Composable ESPHome packages

- Keep `board.yaml` hardware-only: platform, buses, pins and peripherals. Put
  logging, network/radio profiles, fonts, rendering and automations in the demo
  or consuming application.
- For components that support multiple instances (for example `spi`, `i2c`,
  `uart`, `sx126x`, `display` and `binary_sensor`), always use explicit YAML list
  entries, even for one instance. Give each hardware instance a stable `id`.
  Avoid the singleton mapping shorthand for these components: package merging
  happens before schema normalization, so mixing mappings and lists can replace
  the existing definition instead of extending it.
- Consumers modify an existing entry with `- id: !extend <existing_id>` and add
  hardware with a new list entry and distinct ID. Preserve IDs across changes.
- Keep true singleton sections such as `esp32`, `nrf52`, `esphome` and `logger`
  as mappings. Follow each component's schema; do not turn every mapping into
  a list.
- When changing package structure, validate the merged demo and an application
  that extends an existing ID and adds another instance. Inspect the resulting
  configuration to ensure the original hardware and new instance both survive.

## Verification

Run `yamllint boards/<board-slug>`,
`esphome config boards/<board-slug>/demo.yaml` and, for firmware changes,
`esphome compile boards/<board-slug>/demo.yaml`. Describe compilation and physical
hardware testing separately. Keep credentials and generated build files out of
Git. Do not flash a device just to validate a package edit.
