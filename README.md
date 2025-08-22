# ESPHomeCollection

Reusable, hardware-only ESPHome board definitions with simple demos. Keep hardware definition minimal and separate from application logic so users can compose clean projects.

## Available Boards

All board configurations are in the [`boards` directory](./boards/). Each board will be in a `boards/<board-slug>/` directory, with at least:

  * `board.yaml`: the hardware definition. No application logic, automation, api or wifi provisioning. 
  * `demo.yaml`: a simple firmware that illustrates and exercises the board components.

The board slug is lowercase, hyphenated (e.g., `esp32-s3-box-3`, `esp32-c3-devkitm-1`).


## Usage

To use a board definition in your own project, include them as a package like this:

```yaml
packages:
  board: github://fortuna/ESPHomeCollection/boards/esp32-s3-box-3/board.yaml@main
```

Replace `esp32-s3-box-3` with the directory name of the board you want to use.

It's recommended to replace `@main` with a specific commit, in order to avoid breakages
from possibly backwards-imcompatible changes.

See [ESPHome Packages] for details on how package imports work.

[ESPHome Packages]: https://esphome.io/components/packages.html

## Trying out the demos

Each board has a `demo.yaml` config for a demo application that exercises the board definition.
You can run with the command below after you clone the repository:

```sh
esphome run ./boards/${BOARD}/demo.yaml
```

If you don't want to explicitly clone the repository, create a local file (e.g. `demo.yaml`), where the entire content is the import of the demo:

```yaml
# demo.yaml
packages:
  board: github://fortuna/ESPHomeCollection/boards/esp32-s3-box-3/demo.yaml@main
```

Again, replace `esp32-s3-box-3` with the directory name of the demo you want to run.

Then run it from your local file. For example:

```sh
esphome run ./demo.yaml
```

## Development

Contributions of new boards are welcome.

### Install the tooling

```sh
pip install esphome yamllint
```

You may need to use `pip3` or `pipx` depending on your system.

On macOS, if you have [Homebrew installed](https://brew.sh/), use:

```sh
brew install esphome yamllint
```

### Add a new board

1. **Create folder**: `boards/<board-slug>/`, where `<oard-slug>` is lowercase, hyphenated (e.g., `esp32-s3-box-3`, `esp32-c3-devkitm-1`).
1. **Author `board.yaml`** (hardware only):
    * No `esphome:` entry.
    * No `wifi:`, `api`, `ota`, `logger`, etc.
    * `esp32:` block set for the exact devkit and `esp-idf` framework, for example:
      ```yaml
      esp32:
        board: esp32-c3-devkitm-1
        framework:
          type: esp-idf
      ```
    * Define all the harware components (pins, buses, sensors, displays, audio, etc)
    * **No app logic**, including logging and automations.

1. **Author `demo.yaml`** (minimal, friendly):
    * Include the board and add the `esphome` and `logger` blocks:

      ```yaml
      packages:
        board: !include ./board.yaml

      esphome:
        name: board-demo
        friendly_name: Board Demo

      logger:
        level: DEBUG
      ```
    * Include minimal features to exercise hardware. Try to exercise all hardware components if possible. No `wifi`.

1. **Run checks**
    * Run linter:
      ```sh
      yamllint boards/<board>
      ```
      The YAML style is defined in [.yamllint](./.yamllint).

    * Build:
      ```sh
      esphome compile boards/<board>/demo.yaml
      ```
      This must use the `demo.yaml` because the board config is incomplete.

1. Flash it into an actual device to verify it works.
      ```sh
      esphome run boards/<board>/demo.yaml
      ```

   <!-- 1. **Docs**:
   * Update **README** “Available Boards” with the new directory and a one-line description. -->

1. **Submit PR**:
   * Title: `[board] <board-slug>: add board + demo`
   * Ensure the tests pass.

Note: You can quickly validate all configs and lint them in one command:

```sh
esphome config boards/*/demo.yaml && yamllint .
```

To build all the boards, it's recommended to set up a build cache:
```sh
export PLATFORMIO_BUILD_CACHE_DIR=/tmp/esphome_cache
esphome build boards/*/demo.yaml
```

### Clean up

To remove the generated files

```sh
rm -rf boards/*/{.esphome,.gitignore}
```

## TODO
  - Add ESP32-C6 dev board
  - Create nice index table
