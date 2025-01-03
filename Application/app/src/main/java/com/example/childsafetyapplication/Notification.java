package com.example.childsafetyapplication;

/**
 * Represents a notification entry in the database.
 */
public class Notification {
    private String message;
    private String timestamp;
    private boolean disclosed;

    /**
     * Constructs a new Notification object.
     *
     * @param message   The message content of the notification.
     * @param timestamp The timestamp of when the notification was created.
     * @param disclosed Whether the notification has been disclosed (true/false).
     */
    public Notification(String message, String timestamp, boolean disclosed) {
        this.message = message;
        this.timestamp = timestamp;
        this.disclosed = disclosed;
    }

    /**
     * @return The notification message.
     */
    public String getMessage() {
        return message;
    }

    /**
     * @return The timestamp of the notification.
     */
    public String getTimestamp() {
        return timestamp;
    }

    /**
     * @return Whether the notification has been disclosed.
     */
    public boolean isDisclosed() {
        return disclosed;
    }
}