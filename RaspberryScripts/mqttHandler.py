import time
import paho.mqtt.client as mqtt

class MQTThandler:
    def __init__(self, broker="tcp://broker.hivemq.com", port=1883, pub_topic="iotlab/notifications"):
        self.port = port
        self.broker = broker
        self.pub_topic = pub_topic
        self.client = mqtt.Client()  # MQTT Client

        # Setup MQTT client callbacks
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log

        # Connect to MQTT broker
        print("Attempting to connect to broker " + self.broker)
        self.client.connect(self.broker)  # Broker address
        self.client.loop_start()  # Start the loop to handle MQTT callbacks

    def connect_to_broker(self):
        """Attempt to connect to the MQTT broker with retries."""
        while True:
            try:
                print(f"Attempting to connect to broker {self.broker}:{self.port}")
                self.client.connect(self.broker, self.port, keepalive=60)
                self.client.loop_start()  # Start the loop to handle MQTT callbacks
                break  # Exit loop if connection is successful
            except Exception as e:
                print(f"Connection failed: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            print("Connected to MQTT broker!")
        else:
            print(f"Failed to connect, return code: {rc}")

    def on_publish(self, client, userdata, mid):
        """Callback for when a message is successfully published."""
        print(f"Message {mid} published.")

    def on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker."""
        if rc != 0:
            print(f"Unexpected disconnection. Code: {rc}")
        else:
            print("Disconnected from broker.")

    def on_log(self, client, userdata, level, buf):
        """Callback for logging MQTT client activity."""
        print(f"MQTT Log: {buf}")

    def send_notification(self, message):
        """Send a notification to the MQTT broker."""
        print(f"Publishing message to topic {self.pub_topic}: {message}")
        self.client.publish(self.pub_topic, message)
        print(f"Notification sent: {message}")


if __name__ == "__main__":
    mqtt_handler = MQTThandler()  # Initialize MQTT handler

    while True:
        message = "Test Notification"
        mqtt_handler.send_notification(message)  # Send notification
        time.sleep(2.0)  # Set delay