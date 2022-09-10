import time
from datetime import datetime
from typing import Tuple

from smbus2 import SMBus


class RelativeHumidityReading:
    def __init__(self, value: float, timestamp: float):
        self.value = value
        self.timestamp = timestamp
        self.units = "%"

    def __str__(self) -> str:
        return f"{self.value}{self.units}"


class TemperatureReading:
    def __init__(self, value: float, timestamp: float):
        self.value = value
        self.timestamp = timestamp
        self.units = "C"

    def __str__(self) -> str:
        return f"{self.value}{self.units}"


class InitialisationError(Exception):
    pass


class DHT20Sensor:
    def __init__(self, address=0x38):
        self.address = address

        # Wait for sensor to stabilise and reach idle state
        time.sleep(0.2)

        with SMBus(1) as bus:
            status_byte = bus.read_i2c_block_data(self.address, 0x71, 1)

        if status_byte[0] & 0x18 != 0x18:
            raise InitialisationError("Sensor is not initialised")

        time.sleep(0.2)

    def read(self) -> Tuple[TemperatureReading, RelativeHumidityReading]:
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.address, 0xAC, [0x33, 0x00])
            time.sleep(0.1)
            data = bus.read_i2c_block_data(self.address, 0x71, 7)

        reading_time = datetime.utcnow().timestamp()
        temperature = TemperatureReading(self._extract_temperature(data), reading_time)
        humidity = RelativeHumidityReading(self._extract_humidity(data), reading_time)

        return (temperature, humidity)

    def _extract_temperature(self, data: list) -> float:
        raw_temperature = ((data[3] & 0xF) << 16) + (data[4] << 8) + data[5]

        return 200 * (float(raw_temperature) / (2 ** 20)) - 50

    def _extract_humidity(self, data: list) -> float:
        raw_humidity = (data[1] << 12) + (data[2] << 4) + ((data[3] & 0xF0) >> 4)

        return 100 * (float(raw_humidity) / (2 ** 20))
