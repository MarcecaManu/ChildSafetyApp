package com.example.childsafetyapplication;

/**
 * Represents a notification entry in the database.
 */
public class Notification {

    private int id;
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
        this.id = -1;
        this.message = message;
        this.timestamp = timestamp;
        this.disclosed = disclosed;
    }

    /**
     * Constructs an already existing Notification object (it's possible to specify the id).
     *
     * @param id        The unique id of the notification.
     * @param message   The message content of the notification.
     * @param timestamp The timestamp of when the notification was created.
     * @param disclosed Whether the notification has been disclosed (true/false).
     */
    public Notification(int id, String message, String timestamp, boolean disclosed){
        this.id = id;
        this.message = message;
        this.timestamp = timestamp;
        this.disclosed = disclosed;
    }

    /**
     * @return The notification id.
     */
    public int getId() {
        return id;
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