"""Support for awair Sensors."""
import logging
import requests
import paho.mqtt.client as mqtt
import json
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_MONITORED_CONDITIONS)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle



_LOGGER = logging.getLogger(__name__)

CONF_SCAN_INTERVAL = 'scan_interval'
CONF_DEVICES = 'devices'
CONF_ID   = 'id'
CONF_IP   = 'ip'

BSE_URL      = 'http://{}/air-data/latest'
SETTINGS_URL = 'http://{}/settings/config/data'

DEFAULT_NAME        = 'awair'

MIN_TIME_BETWEEN_SENSOR_UPDATES = timedelta(seconds=300)
SCAN_INTERVAL = timedelta(seconds=10)

_AWAIR_PROPERTIES = {
  'score': ['Score',       None,    'mdi:periodic-table'],
  'temp':  ['Temperature', '°C',    'mdi:thermometer'],
  'humid': ['Humidity',    '%',     'mdi:water-percent'],
  'co2':   ['CO₂',         'ppm',   'mdi:periodic-table-co2'],
  'voc':   ['VOC',         'ppb',   'mdi:chemical-weapon'],
  'pm25':  ['PM2.5',       '㎍/㎥', 'mdi:blur'],
  'lux':   ['Light',       'lux',   'mdi:weather-sunny'],
  'spl_a': ['Noise',       'dBA',   'mdi:volume-vibrate'],
  "device_uuid": ['Device UUID', None, 'mdi:devices'],
  "wifi_mac":    ['Wifi mac',    None, 'mdi:wifi'],
  "ssid":        ['SSID',        None, 'mdi:wifi'],
  "ip":          ['IP',          None, 'mdi:ip'],
  "netmask":     ['Netmask',     None, 'mdi:alpha-n-box-outline'],
  "gateway":     ['Gateway',     None, 'mdi:alpha-g-box-outline'],
  "fw_version":  ['Firmware',    None, 'mdi:alpha-f-box-outline'],
  "timezone":    ['Timezone',    None, 'mdi:alpha-t-box-outline'],
  "display":     ['Display',     None, 'mdi:alpha-d-box-outline'],
  "led":         ['Led',         None, 'mdi:alpha-l-box-outline']
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period,
    vol.Required(CONF_DEVICES): vol.All(cv.ensure_list, [{
        vol.Required(CONF_ID,   default= ''): cv.string,
        vol.Required(CONF_NAME, default= ''): cv.string,
        vol.Required(CONF_IP,   default= ''): cv.string,
    }]),
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up a awair Sensors."""
    name    = config.get(CONF_NAME)
    devices = config.get(CONF_DEVICES)

    SCAN_INTERVAL = config.get(CONF_SCAN_INTERVAL)

    sensors = []

    for awair in devices:
        api = awairAPI(awair[CONF_NAME], awair[CONF_IP])

        sensor = awairSensor(awair[CONF_ID], awair[CONF_NAME], awair[CONF_IP], api)

        sensor.update()

        sensors += [sensor]

        for key, value in sensor._data.items():
            sensors += [awairPropSensor(awair[CONF_ID], key, value, sensor)]

    add_entities(sensors, True)


class awairAPI:
    """awair API."""

    def __init__(self, name, ip):
        """Initialize the awair API.."""
        self._name = name
        self._ip   = ip

        self.data = {}

    def update(self):
        """Update function for updating api information."""
        try:
            #air-data/data
            url = BSE_URL.format(self._ip)

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            awair = response.json()

            self.data = awair

            #settings/config/data
            url = SETTINGS_URL.format(self._ip)

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            config = response.json()

            for key, value in config.items():
                self.data[key] = value

        except Exception as ex:
            _LOGGER.error('Failed to update awair API status Error: %s', ex)
            raise


class awairSensor(Entity):
    """Representation of a awair Sensor."""

    def __init__(self, id, name, ip, api):
        """Initialize the awair sensor."""
        self._id   = id
        self._name = name
        self._ip   = ip

        self._api  = api

        self._data = {}

        self._icon = 'mdi:blur-linear'

    @property
    def entity_id(self):
        """Return the entity ID."""
        return 'sensor.awair_{}'.format(self._id)

    @property
    def name(self):
        """Return the name of the sensor, if any."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._data['score']

    @Throttle(MIN_TIME_BETWEEN_SENSOR_UPDATES)
    def update(self):
        """Get the latest state of the sensor."""
        if self._api is None:
            return

        self._api.update()

        self._data = self._api.data


    @property
    def device_state_attributes(self):
        """Attributes."""
        attr = {}

        for key in self._data:
            attr[_AWAIR_PROPERTIES[key][0]] = '{}{}'.format(self._data[key], '' if _AWAIR_PROPERTIES[key][1] is None else ' {}'.format(_AWAIR_PROPERTIES[key][1]) )

        #attr['IP'] = self._ip

        return attr


class awairPropSensor(Entity):
    """awair Properties sensor"""
    def __init__(self, id, key, value, awair):
        self._id    = id

        self._key   = key
        self._value = value

        self._awair = awair

    @property
    def entity_id(self):
        return 'sensor.awair_{}_{}'.format(self._id, self._key)

    @property
    def name(self):
        return _AWAIR_PROPERTIES[self._key][0]

    @property
    def icon(self):
        return _AWAIR_PROPERTIES[self._key][2]

    @property
    def state(self):
        return self._value

    @Throttle(SCAN_INTERVAL)
    def update(self):

        if self._awair is None:
            return

        self._value = self._awair._data[self._key]

    @property
    def device_state_attributes(self):
        """Attributes."""
        attr = {}

        attr[self._key] = self._value

        return attr

