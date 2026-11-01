# Contributing

Add reusable hardware packages under `boards/<board-slug>/`, with a minimal
`demo.yaml` beside each `board.yaml`. Use lowercase, hyphenated board slugs such
as `esp32-s3-box-3`. See [README.md](README.md) for package usage and running demos.

## Install the tooling

Use Python 3.12 or newer for current ESPHome releases:

```sh
pip install esphome yamllint
```

On macOS with Homebrew:

```sh
brew install esphome yamllint
```

## Board and package conventions

- Keep `board.yaml` hardware-only: platform, buses, pins and peripherals. No
  `esphome`, `wifi`, `api`, `ota`, `logger` or application automations.
- For ESP32 boards, select the exact board and `framework.type: esp-idf`. Document
  compatibility profiles and unsupported capabilities explicitly for other MCUs.
- Put logging, network/radio profiles, fonts, rendering, button actions and startup
  power policy in the demo or consuming application. Define the power-control pin
  and polarity in the board; let the application choose when to enable the rail.
- For components that support multiple instances (for example `spi`, `i2c`,
  `uart`, `sx126x`, `display` and `binary_sensor`), use explicit YAML list entries,
  even for one instance. Give each hardware instance a stable `id`. Package merging
  happens before schema normalization, so mixing mapping shorthand and lists can
  replace the existing definition instead of extending it.
- Consumers modify an existing entry with `- id: !extend <existing_id>` and add
  hardware with a new list entry and distinct ID. Preserve IDs across changes.
- Keep singleton sections such as `esp32`, `nrf52`, `esphome` and `logger` as
  mappings. Follow each component's schema; do not turn every mapping into a list.
- Use two-space YAML indentation and no tabs. The full style is in
  [.yamllint](.yamllint).
- Keep demos minimal and offline by default, without Wi-Fi credentials or secrets.
  Keep generated firmware, build files and private backups out of Git.
- Board READMEs describe hardware capabilities, source references, exceptions and
  verification limits. Link to the root README for shared usage and this guide
  for development instructions instead of repeating them.

## Add a board

Create `boards/<board-slug>/board.yaml` using the conventions above. Then add
`demo.yaml`, including the board and defining the application settings:

```yaml
packages:
  board: !include board.yaml

esphome:
  name: board-demo
  friendly_name: Board Demo

logger:
  level: DEBUG
```

Exercise the defined hardware where practical. Document anything the demo leaves
untested or unsupported in the board README.

## Validate and build

Run these commands from the repository root, replacing `<board-slug>`:

```sh
yamllint boards/<board-slug>
esphome config boards/<board-slug>/demo.yaml
esphome compile boards/<board-slug>/demo.yaml
```

Validate the demo rather than `board.yaml`: the hardware package is intentionally
incomplete without application configuration. When changing package structure,
also validate a consumer that extends an existing ID and adds another instance.
Inspect the merged output to ensure the original hardware and new instance survive.

Validate and lint the full collection:

```sh
esphome config boards/*/demo.yaml
yamllint .
```

Compile all demos, with a cache for PlatformIO builds:

```sh
export PLATFORMIO_BUILD_CACHE_DIR=/tmp/esphome_cache
esphome compile boards/*/demo.yaml
```

For physical verification, follow [running demos](README.md#trying-out-the-demos)
on the intended device. Flashing replaces its application firmware; preserve
existing firmware/state first. Do not flash just to validate a package edit.
Report configuration validation, compilation and physical testing separately;
a successful build does not establish hardware support.

## Submit a pull request

- Use a scoped, imperative commit message.
- Title new-board PRs `[board] <board-slug>: add board + demo`.
- Describe hardware support, demo behavior, caveats, toolchain versions and checks
  performed. State which hardware interactions have been observed and which are
  still untested; include logs or screenshots when useful.
- Keep board documentation and verification evidence aligned with the final change.

## Clean up

Remove a demo's generated build files with:

```sh
esphome clean boards/<board-slug>/demo.yaml
```
