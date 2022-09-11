# dht20-sensor
Code for taking readings with the DHT20 temperature humidity sensor using I2C.

This is the most basic working implementation that suits my needs. It doesn't handle sensor initialisation.

## Example Usage

```
import time

from dht20_sensor.sensor import DHT20Sensor

if __name__ == "__main__":
    sensor = DHT20Sensor()

    while True:
        t, h = sensor.read()
        print(t)
        print(h)
        time.sleep(2)

```
