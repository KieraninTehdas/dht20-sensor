from unittest import mock

import pytest

from src.dht20_sensor.sensor import DHT20Sensor, InitialisationError


@mock.patch("src.dht20_sensor.sensor.SMBus", autospec=True)
class TestSensor:
    def test_init_when_sensor_is_not_initialised(self, smbus_mock):
        smbus_mock.read_i2c_block_data.return_value = [0x1]

        with pytest.raises(InitialisationError):
            DHT20Sensor()
