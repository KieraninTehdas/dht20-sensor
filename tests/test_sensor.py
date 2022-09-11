from unittest import mock
from datetime import datetime

import pytest

from src.dht20_sensor.sensor import DHT20Sensor, InitialisationError


@mock.patch("src.dht20_sensor.sensor.SMBus", autospec=True)
class TestSensor:
    valid_data = [0x1C, 0xBA, 0xC8, 0x5, 0xCC, 0xE3, 0x28]

    def test_init_when_sensor_is_not_initialised(self, smbus_mock):
        smbus_mock.return_value.__enter__.return_value.read_i2c_block_data.return_value = [
            0x1
        ]

        with pytest.raises(InitialisationError):
            DHT20Sensor()

    def test_returns_correct_values(self, smbus_mock):
        smbus_mock.return_value.__enter__.return_value.read_i2c_block_data.side_effect = [
            [0x18],
            self.valid_data,
        ]

        temperature, humidity = DHT20Sensor().read()

        assert temperature.value == 22.5
        assert humidity.value == 73.0

    @mock.patch("src.dht20_sensor.sensor.datetime", autospec=True)
    def test_sets_timestamp_to_utc_now(self, datetime_mock, smbus_mock):
        now = datetime.utcnow()
        datetime_mock.utcnow = mock.Mock(return_value=now)
        smbus_mock.return_value.__enter__.return_value.read_i2c_block_data.side_effect = [
            [0x18],
            self.valid_data,
        ]

        temperature, humidity = DHT20Sensor().read()

        assert temperature.timestamp == now.timestamp()
        assert humidity.timestamp == now.timestamp()
