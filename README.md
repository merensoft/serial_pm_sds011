# Serial Particulate Matter SDS011 Sensor

Particulate matter sensors measure the amount of very small particles in the air.

Cheap LED based sensors usually use a GPIO interface that is hard to attach to computers. 
However, there are a lot of laser LED based sensors on the market that use a serial interface 
and can be connected to your Home Assistant system easily with a USB to serial converter.

## Supported Sensors
At this time, the following sensors are supported:

- sds011
- sds021
  
## Configuration
To use your PM sensor in your installation, add the following to your configuration.yaml file:

```yaml
sensor:
  - platform: serial_pm_sds011
    scan_interval: 60
    port: "/dev/cu.usbserial-11230"
    name: "SDS011"
    unique_id: "sds011_sensor"
```

### Build with :heart: By Merensoft
