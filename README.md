# ESPHomeCollection

This repository is where I share reusable ESPHome YAML definitions for various
boards and dev kits I acquire, to make it easier for others to use those boards.

## Core Principle

My board definitions are clean, only defining the hardware. That allows you to
focus on the application logic. This separation of hardware and application
makes the code reusable and composable.

## Available Boards

You can find all board configurations in the [`boards` directory](./boards/). Each board has a
`board.yaml` for the hardware definition and a `demo.yaml` for a sample application.

## Using a Board Definition in Your Project

To use a board definition in your own project, include them as a package like this:

```yaml
packages:
  board: github://fortuna/ESPHomeCollection/boards/esp32-s3-box-3/board.yaml@main
```

Replace `esp32-s3-box-3` with the directory name of the board you want to use.

See [ESPHome Packages] for how package imports work.

[ESPHome Packages]: https://esphome.io/components/packages.html

## Trying out the demos

Each board has a `demo.yaml` config for a demo application that exercises the board definition.
You can run with the command below after you clone the repository:

```sh
esphome run ./boards/${BOARD}/demo.yaml
```

If you don't want to explicitly clone the repository, create a local file (e.g. `demo.yaml`), where the entire content is the import of the demo:

```yaml
packages:
  board: github://fortuna/ESPHomeCollection/boards/esp32-s3-box-3/demo.yaml@main
```

Again, replace `esp32-s3-box-3` with the directory name of the demo you want to run.

Then run it from your local file. For example:

```sh
esphome run ./demo.yaml
```

## Development

You need to install the `esphome` and `yamllint` Python binaries.

On macOS, if you have Homebrew installed, you can use:

```sh
brew install esphome yamllint
```

On other platforms, it may be easier to use `pipx run`, but you need `pipx` installed.

To quickly validate a config, use `esphome config`. For example:

```sh
esphome config boards/esp32-s3-box-3/demo.yaml
```

You must run `esphome config` on the demo files, because the board definitions are incomplete ESPHome configs and will fail validation.

To lint all files:

```sh
yamllint .
```

You can validate all configs and lint them in one command:

```sh
esphome config boards/*/demo.yaml && yamllint .
```

## TODO
  - Add demos and test:
    - M5Stack Atom Echo
  - Add ESP32-C6 dev board
  - Create nice index table
