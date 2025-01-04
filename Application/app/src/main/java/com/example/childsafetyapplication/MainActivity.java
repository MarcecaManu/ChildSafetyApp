package com.example.childsafetyapplication;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

/**
 * MainActivity is the primary entry point for the Child Safety Application.
 * It handles MQTT connections for real-time alerts, manages notifications, and provides navigation
 * to other activities such as the camera feed and notifications history.
 */
public class MainActivity extends AppCompatActivity {

    private MqttAndroidClient client; // MQTT client for managing real-time notifications
    private static final String SERVER_URI = "tcp://broker.hivemq.com:1883"; // MQTT broker URI
    private static final String TAG = "MainActivity"; // Logging tag
    private static final String CHANNEL_ID = "child_safety_channel"; // Notification channel ID

    /**
     * Connects to the MQTT broker.
     * Establishes a session with the specified broker and logs the connection status.
     */
    private void connect() {
        String clientId = MqttClient.generateClientId();
        client = new MqttAndroidClient(this.getApplicationContext(), SERVER_URI, clientId);
        try {
            IMqttToken token = client.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    Log.d(TAG, "onSuccess");
                    System.out.println(TAG + " Success. Connected to " + SERVER_URI);
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.d(TAG, "onFailure");
                    System.out.println(TAG + " Oh no! Failed to connect to " + SERVER_URI);
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    /**
     * Subscribes to a specified MQTT topic to receive notifications.
     *
     * @param topicToSubscribe The MQTT topic to subscribe to.
     */
    private void subscribe(String topicToSubscribe) {
        final String topic = topicToSubscribe;
        int qos = 1; // Quality of Service level
        try {
            IMqttToken subToken = client.subscribe(topic, qos);
            subToken.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    System.out.println("Subscription successful to topic: " + topic);
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    System.out.println("Failed to subscribe to topic: " + topic);
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    /**
     * Creates a notification channel for Android 8.0 (API level 26) and higher.
     * The channel is used for displaying notifications related to child safety alerts.
     */
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = getString(R.string.channel_name);
            String description = getString(R.string.channel_description);
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, importance);
            channel.setDescription(description);
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
    }

    /**
     * Sends a notification to the user.
     *
     * @param message The content of the notification.
     */
    private void sendNotification(String message) {
        final String notificationTitle = "CHILD SAFETY ALERT";

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.drawable.notification)
                .setContentTitle(notificationTitle)
                .setContentText(message)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setAutoCancel(true);

        NotificationManager notificationManager = getSystemService(NotificationManager.class);
        notificationManager.notify(1, builder.build());
    }

    /**
     * Called when the activity is first created.
     * Sets up the UI, initializes the MQTT client, and configures button listeners.
     *
     * @param savedInstanceState If the activity is being re-initialized after previously being shut down,
     *                           this Bundle contains the most recent data supplied by onSaveInstanceState.
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        // Apply system bar insets
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Initialize the database and clean up expired notifications
        DBHelper db = new DBHelper(this);
        db.deleteExpiredNotifications();

        // Set up the button to open the camera activity
        Button openCameraButton = findViewById(R.id.btn_open_camera);
        openCameraButton.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, CameraActivity.class);
            startActivity(intent);
        });

        // Set up the button to view notifications history
        Button viewNotificationsButton = findViewById(R.id.btn_notifications);
        viewNotificationsButton.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, NotificationsActivity.class);
            startActivity(intent);
        });

        // Set up the notification channel and connect to MQTT broker
        createNotificationChannel();
        connect();

        // Set MQTT callback to handle message events
        client.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                if (reconnect) {
                    System.out.println("Reconnected to : " + serverURI);
                    subscribe("iot/notifications");
                } else {
                    System.out.println("Connected to: " + serverURI);
                    subscribe("iot/notifications");
                }
            }

            @Override
            public void connectionLost(Throwable cause) {
                System.out.println("The connection was lost.");
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                String newMessage = new String(message.getPayload());
                System.out.println("Incoming message: " + newMessage);

                // Send a notification to the user
                sendNotification(newMessage);

                // Save the notification to the database
                Notification notification = new Notification(
                        newMessage, DBHelper.getCurrentTimestamp(), false);
                db.addNotification(notification);
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
            }
        });
    }
}
