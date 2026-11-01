# Copyright 2026 Vinicius Fortuna
# SPDX-License-Identifier: Apache-2.0
"""Remove foreign peripheral wiring from the nRF52840 compatibility profile."""

import esphome.config_validation as cv
from esphome.components.zephyr import zephyr_add_overlay, zephyr_add_prj_conf

DEPENDENCIES = ["nrf52"]
CONFIG_SCHEMA = cv.Schema({})


async def to_code(config):
    # The ItsyBitsy's external flash, DotStar, buses and aliases are not T096
    # hardware. Its QSPI pins overlap the T096's radio/display/GNSS pins.
    # This is a GPIO-only port; physical T096 GPIOs remain in board.yaml.
    zephyr_add_overlay('''
        / {
            model = "Heltec Mesh Node T096 (GPIO bring-up)";
            leds { status = "disabled"; };
            buttons { status = "disabled"; };
            aliases {
                /delete-property/ led0;
                /delete-property/ sw0;
                /delete-property/ led-strip;
            };
            chosen {
                /delete-property/ zephyr,ieee802154;
            };
        };
        &qspi { status = "disabled"; };
        &gd25q16 { status = "disabled"; };
        &spi1 { status = "disabled"; };
        &spi2 { status = "disabled"; };
        &apa102 { status = "disabled"; };
        &i2c0 { status = "disabled"; };
        &uart0 { status = "disabled"; };
        &adc { status = "disabled"; };
        &ieee802154 { status = "disabled"; };
    ''')
    zephyr_add_prj_conf("NORDIC_QSPI_NOR", False)
