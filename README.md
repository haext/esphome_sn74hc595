# esphome_sn74hc595

An improved fork of the [sn74hc595 component](https://esphome.io/components/sn74hc595.html) for ESPHome.

### Changes from the base component:

* `sn74hc595` becomes `sn74hc595i` in your configuration file
* Pins with `inverted: true` will have the correct state on reset. In short `restore_mode` plays nice with `inverted`.  This avoids relays pulsing on boot-up and reset.
* Adds `save_writes` to avoid toggling the pin when not necessary, useful when using the 74hc595 on slow interfaces like i2c gpio extenders.

## How to use

* Add the external component as shown in [the example](#example)

### Example

```
external_components:
  - source: github://haext/esphome_sn74hc595

sn74hc595i:
  - id: 'sn74hc595_hub'
    latch_pin: D7
    oe_pin: D6
    sr_count: 2

switch:
  - platform: gpio
    name: "SN74HC595 Pin #0"
    save_writes: true
    pin:
      sn74hc595: sn74hc595_hub
      number: 0
      inverted: true
```
