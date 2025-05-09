import paho.mqtt.client as mqtt
import time
import random

class device:
    def __init__(self, name, device_type, group, location, mqtt_broker, port=1883):
        self.name = name
        self.type = device_type
        self.group = group
        self.location = location
        self.topic = f"{location}/{group}/{device_type}/{name}"
        self.status_topic = f"{self.topic}/status"
        self.broker = mqtt_broker
        self.port = port
        self.client = mqtt.Client()
        self.current_status = None
        
        self.client.on_message = self.handle_message
    
    def handle_message(self, client, userdata, message):
        if message.topic == self.status_topic:
            self.current_status = message.payload.decode()
    
    def connect(self):
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
            self.client.subscribe(self.status_topic)
            print(f"{self.name} connected!")
        except Exception as e:
            print(f"Couldn't connect {self.name}: {e}")
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print(f"{self.name} disconnected.")
    
    def turn_on(self):
        self.client.publish(self.topic, "Turn_on")
        print(f"{self.name} turned ON")
    
    def turn_off(self):
        self.client.publish(self.topic, "Turn_off")
        print(f"{self.name} turned OFF")
    
    def get_status(self, wait_time=2):
        self.client.publish(self.topic, "status_request")
        time.sleep(wait_time)
        return self.current_status if self.current_status else "unknown"

class sensor:
    def __init__(self, name, sensor_type, group, location, pin=4):
        self.name = name
        self.type = sensor_type
        self.group = group
        self.location = location
        self.pin = pin
        self.last_value = None
    
    def read(self):
        # Simulate sensor reading for simplicity
        self.last_value = random.uniform(20, 30) if self.type == "thermometer" else random.uniform(40, 60)
        return self.last_value

class admin:
    def __init__(self):
        self.devices = []
        self.sensors = []
    
    def add_device(self, name, device_type, group, location, mqtt_broker, port=1883):
        new_device = device(name, device_type, group, location, mqtt_broker, port)
        new_device.connect()
        self.devices.append(new_device)
        print(f"Added device: {name}")
    
    def add_sensor(self, name, sensor_type, group, location, pin=4):
        new_sensor = sensor(name, sensor_type, group, location, pin)
        self.sensors.append(new_sensor)
        print(f"Added sensor: {name}")
    
    def turn_on_group(self, group_name):
        for device in self.devices:
            if device.group == group_name:
                device.turn_on()
    
    def turn_off_group(self, group_name):
        for device in self.devices:
            if device.group == group_name:
                device.turn_off()
    
    def turn_on_all(self):
        for device in self.devices:
            device.turn_on()
    
    def turn_off_all(self):
        for device in self.devices:
            device.turn_off()
            
    def get_group_sensor_data(self, group_name):
        results = {}
        for sensor in self.sensors:
            if sensor.group == group_name:
                results[sensor.name] = sensor.read()
        return results
    
    def get_group_device_status(self, group_name):
        statuses = []
        for device in self.devices:
            if device.group == group_name:
                statuses.append(f"{device.name}: {device.get_status()}")
        return ", ".join(statuses)
