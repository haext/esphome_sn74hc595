import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import spi
from esphome.const import (
    CONF_ID,
    CONF_SPI_ID,
    CONF_NUMBER,
    CONF_INVERTED,
    CONF_DATA_PIN,
    CONF_CLOCK_PIN,
    CONF_OUTPUT,
)
from esphome.core import EsphomeError

MULTI_CONF = True

sn74hc595i_ns = cg.esphome_ns.namespace("sn74hc595i")

SN74HC595IComponent = sn74hc595i_ns.class_("SN74HC595IComponent", cg.Component)
SN74HC595IGPIOComponent = sn74hc595i_ns.class_(
    "SN74HC595IGPIOComponent", SN74HC595IComponent
)
SN74HC595ISPIComponent = sn74hc595i_ns.class_(
    "SN74HC595ISPIComponent", SN74HC595IComponent, spi.SPIDevice
)

SN74HC595IGPIOPin = sn74hc595i_ns.class_(
    "SN74HC595IGPIOPin", cg.GPIOPin, cg.Parented.template(SN74HC595IComponent)
)

CONF_SN74HC595I = "sn74hc595i"
CONF_LATCH_PIN = "latch_pin"
CONF_OE_PIN = "oe_pin"
CONF_SR_COUNT = "sr_count"
CONF_SAVE_WRITES = "save_writes"

CONFIG_SCHEMA = cv.Any(
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(SN74HC595IGPIOComponent),
            cv.Required(CONF_DATA_PIN): pins.gpio_output_pin_schema,
            cv.Required(CONF_CLOCK_PIN): pins.gpio_output_pin_schema,
            cv.Required(CONF_LATCH_PIN): pins.gpio_output_pin_schema,
            cv.Optional(CONF_OE_PIN): pins.gpio_output_pin_schema,
            cv.Optional(CONF_SR_COUNT, default=1): cv.int_range(min=1, max=256),
            cv.Optional(CONF_SAVE_WRITES, default=False): cv.boolean,
        }
    ).extend(cv.COMPONENT_SCHEMA),
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(SN74HC595ISPIComponent),
            cv.Required(CONF_LATCH_PIN): pins.gpio_output_pin_schema,
            cv.Optional(CONF_OE_PIN): pins.gpio_output_pin_schema,
            cv.Optional(CONF_SR_COUNT, default=1): cv.int_range(min=1, max=256),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(spi.spi_device_schema(cs_pin_required=False))
    .extend(
        {
            cv.Required(CONF_SPI_ID): cv.use_id(spi.SPIComponent),
        }
    ),
    msg='Either "data_pin" and "clock_pin" must be set or "spi_id" must be set.',
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    if CONF_DATA_PIN in config:
        data_pin = await cg.gpio_pin_expression(config[CONF_DATA_PIN])
        cg.add(var.set_data_pin(data_pin))
        clock_pin = await cg.gpio_pin_expression(config[CONF_CLOCK_PIN])
        cg.add(var.set_clock_pin(clock_pin))
    elif CONF_SPI_ID in config:
        await spi.register_spi_device(var, config)
    else:
        raise EsphomeError("Not supported")

    if config.get(CONF_SAVE_WRITES, False):
        cg.add_define("SAVE_WRITES")
    latch_pin = await cg.gpio_pin_expression(config[CONF_LATCH_PIN])
    cg.add(var.set_latch_pin(latch_pin))
    if CONF_OE_PIN in config:
        oe_pin = await cg.gpio_pin_expression(config[CONF_OE_PIN])
        cg.add(var.set_oe_pin(oe_pin))
    cg.add(var.set_sr_count(config[CONF_SR_COUNT]))


def _validate_output_mode(value):
    if value.get(CONF_OUTPUT) is not True:
        raise cv.Invalid("Only output mode is supported")
    return value


SN74HC595I_PIN_SCHEMA = pins.gpio_base_schema(
    SN74HC595IGPIOPin,
    cv.int_range(min=0, max=2047),
    modes=[CONF_OUTPUT],
    mode_validator=_validate_output_mode,
    invertible=True,
).extend(
    {
        cv.Required(CONF_SN74HC595I): cv.use_id(SN74HC595IComponent),
    }
)


def sn74hc595i_pin_final_validate(pin_config, parent_config):
    max_pins = parent_config[CONF_SR_COUNT] * 8
    if pin_config[CONF_NUMBER] >= max_pins:
        raise cv.Invalid(f"Pin number must be less than {max_pins}")


@pins.PIN_SCHEMA_REGISTRY.register(
    CONF_SN74HC595I, SN74HC595I_PIN_SCHEMA, sn74hc595i_pin_final_validate
)
async def sn74hc595i_pin_to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_parented(var, config[CONF_SN74HC595I])

    cg.add(var.set_pin(config[CONF_NUMBER]))
    cg.add(var.set_inverted(config[CONF_INVERTED]))
    return var