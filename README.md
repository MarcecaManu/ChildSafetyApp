# Child Safety Monitoring Application

This project implements an IoT-based child safety monitoring system using sensors, cameras, and smart devices to enhance safety in households. The system tracks child activity in potentially hazardous areas, disables appliances when necessary, and sends real-time notifications and live video feeds to parents.

## Features
- **Sensor Integration:** Utilizes ultrasonic sensors and PIR motion sensors for presence detection.
- **Real-Time Notifications:** Alerts parents when a child is in a potentially dangerous situation.
- **Live Video Streaming:** Streams video from the Raspberry Pi camera module to a mobile application.
- **Appliance Control:** Automatically disables smart plugs in hazardous situations.
- **Room Tracking:** Tracks the number of individuals in the room and determines their direction of movement with an additional ultrasonic sensor.

## Setup

### Prerequisites
1. A Raspberry Pi 4 with GPIO capabilities.
2. At least 3 ultrasonic sensors (e.g., HC-SR04) for basic functionality.
3. An optional fourth ultrasonic sensor for directional movement tracking.
4. PIR motion sensors (e.g., HC-SR501).
5. Raspberry Pi Camera Module 2 for live video streaming.
6. Smart plugs (e.g., Proove TSR101) and a Tellstick ZNet Lite v2 communication module.

### Installation
1. Clone this repository:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure the pins in the `motionHandler.py` and `ultrasonicHandler.py` files to match your hardware setup.

### Configuration
- Verify the GPIO pins assigned for the sensors in the `motionHandler.py` and `ultrasonicHandler.py` scripts.
- If using the camera module, ensure it is enabled in the Raspberry Pi settings and configure port forwarding for remote access.

## Running the Application

- **With 3 Ultrasonic Sensors:**
  Run `main.py` for basic functionality:
  ```bash
  python main.py
  ```
- **With 4 Ultrasonic Sensors:**
  Run `main_w_direction.py` to enable directional tracking of movement through the door:
  ```bash
  python main_w_direction.py
  ```

## Mobile Application
The accompanying mobile application, developed in Android Studio, allows:
1. Viewing real-time video feeds.
2. Receiving and managing notifications.

Ensure the Raspberry Pi's static IP and port forwarding settings are correctly configured for seamless interaction.

## Testing
1. Unit tests were performed for individual components like sensors and actuators.
2. Integration tests validated inter-component communication.
3. Stress tests ensured system reliability during prolonged usage.

## Future Enhancements
- Full integration of the Pi Camera and additional sensors.
- Expand system coverage to multiple rooms.
- Implement a login feature for enhanced security.
- Cloud-based architecture to support multiple users and families.

## Authors
- **Manuel Marceca** (mama9469)
- **Filip Silversten Wärn** (fisi6585)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

---

For more details, refer to the [project report](Child_Safety_Monitoring_Application-Report.pdf).