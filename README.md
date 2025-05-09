# ESPHomeCollection

This repository is where I share reusable ESPHome YAML definitions for various boards and dev kits I acquire, to make it easier for others to use those boards.

My board definition are clean, only define the hardware. That allows you to focus on the application logic. This separation of hardware and application makes the code reusable and composable.

You can find the board configs in the [`boards` directory](./boards). They are all named `board.yaml`.

They each have a `demo.yaml` config for a demo application, which you can run with:

```sh
esphome run ./boards/${BOARD}/demo.yaml
```

TODO:
  - Create index table
  - Add demos
  - Test
