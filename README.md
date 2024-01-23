# esphome_sn74hc595

An improved fork of the [sn74hc595 component](https://esphome.io/components/sn74hc595.html) for ESPHome.

Changes from the base component:

* You must add the external component as shown in [the example](#example)
* `sn74hc595` becomes `sn74hc595i` in your configuration file
* Pins with `inverted: true` will have the correct state on reset. In short `restore_mode` plays nice with `inverted`.  This avoids relays pulsing on boot-up and reset.

# Example

```
external_components:
  - source: github://gdgib/esphome_sn74hc595@v0.0.1

sn74hc595i:
  - id: 'sn74hc595_hub'
    latch_pin: D7
    oe_pin: D6
    sr_count: 2

switch:
  - platform: gpio
    name: "SN74HC595 Pin #0"
    pin:
      sn74hc595: sn74hc595_hub
      number: 0
      inverted: true
```
