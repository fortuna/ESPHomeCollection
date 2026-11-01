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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for tooling, board conventions, validation
and the pull request workflow.

## TODO
  - Add ESP32-C6 dev board
  - Create nice index table
