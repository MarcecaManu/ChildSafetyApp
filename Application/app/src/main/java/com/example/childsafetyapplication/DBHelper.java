package com.example.childsafetyapplication;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Locale;

/**
 * A helper class for managing SQLite database operations for storing and manipulating notifications.
 */
public class DBHelper extends SQLiteOpenHelper {

    private String NOTIFICATIONS_TABLE = "Notifications";

    // Columns
    private String NOTIF_ID = "Notif_ID";
    private String NOTIF_MESSAGE = "Notif_Message";
    private String NOTIF_TIMESTAMP = "Notif_Timestamp";
    private String NOTIF_DISCLOSED = "Notif_Disclosed";

    // Lengths
    private int MAX_LENGTH_NOTIF_MESSAGE = 200;
    private int MAX_LENGTH_NOTIF_TIMESTAMP = 30;

    /**
     * Constructs a new instance of DBHelper.
     *
     * @param context The context of the application using the database.
     */
    public DBHelper(Context context) {
        super(context, "NotificationsDB", null, 1);
    }

    /**
     * Get the current timestamp in a human-readable format
     *
     * @return Timestamp in a human-readable format
     */
    public static String getCurrentTimestamp(){
        // Get the current time in milliseconds
        long currentTimeMillis = System.currentTimeMillis();

        // Format it to a human-readable format (e.g., "yyyy-MM-dd HH:mm:ss")
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());

        // Convert the current time to a formatted string
        String formattedDate = sdf.format(new Date(currentTimeMillis));

        return formattedDate;
    }

    /**
     * Called when the database is created for the first time. Creates the notifications table.
     *
     * @param db The SQLite database instance.
     */
    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE " + NOTIFICATIONS_TABLE + " (" +
                NOTIF_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                NOTIF_MESSAGE + " VARCHAR(" + MAX_LENGTH_NOTIF_MESSAGE + ") NOT NULL, " +
                NOTIF_TIMESTAMP + " VARCHAR(" + MAX_LENGTH_NOTIF_TIMESTAMP + "), " +
                NOTIF_DISCLOSED + " INTEGER)"
        );
    }

    /**
     * Called when the database needs to be upgraded. Recreates the notifications table.
     *
     * @param db         The SQLite database instance.
     * @param old_version The old database version.
     * @param new_version The new database version.
     */
    @Override
    public void onUpgrade(SQLiteDatabase db, int old_version, int new_version) {
        db.execSQL("DROP TABLE IF EXISTS " + NOTIFICATIONS_TABLE);
        onCreate(db);
    }

    /**
     * Adds a new notification to the database.
     *
     * @param notification The Notification object containing the details to be stored.
     */
    public void addNotification(Notification notification) {
        ContentValues contentValues = new ContentValues();
        SQLiteDatabase db = this.getWritableDatabase();

        contentValues.put(NOTIF_MESSAGE, notification.getMessage());
        contentValues.put(NOTIF_TIMESTAMP, notification.getTimestamp());
        contentValues.put(NOTIF_DISCLOSED, notification.isDisclosed() ? 1 : 0);

        db.insert(NOTIFICATIONS_TABLE, null, contentValues);
        db.close();
    }

    /**
     * Updates a notification's disclosed status to 1 (true) for the given ID.
     *
     * @param id The ID of the notification to disclose.
     */
    public void discloseNotifications(int id) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put(NOTIF_DISCLOSED, 1);
        db.update(NOTIFICATIONS_TABLE, contentValues, NOTIF_ID + " = ?", new String[]{String.valueOf(id)});
        db.close();
    }

    /**
     * Deletes a notification from the database based on its ID.
     *
     * @param id The ID of the notification to delete.
     */
    public void deleteNotification(int id) {
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(NOTIFICATIONS_TABLE, NOTIF_ID + " = ?", new String[]{String.valueOf(id)});
        db.close();
    }

    /**
     * Deletes all notifications with a timestamp older than 24 hours.
     */
    public void deleteExpiredNotifications() {
        SQLiteDatabase db = this.getWritableDatabase();
        // Calculate the time 24 hours ago in the same format as the stored timestamps
        String twentyFourHoursAgo = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
                .format(new Date(System.currentTimeMillis() - 86400000L)); // 24 hours in milliseconds

        // Delete notifications older than 24 hours
        db.delete(NOTIFICATIONS_TABLE, NOTIF_TIMESTAMP + " < ?", new String[]{twentyFourHoursAgo});
        db.close();
    }

    /**
     * Deletes all disclosed notifications.
     */
    public void deleteDisclosedNotifications() {
        SQLiteDatabase db = this.getWritableDatabase();

        // Delete notifications older than 24 hours
        db.delete(NOTIFICATIONS_TABLE, NOTIF_DISCLOSED + " = 1", null);
        db.close();
    }

    /**
     * Retrieves all notifications in an ArrayList sorted by timestamp (newest to oldest).
     *
     * @return ArrayList of notification, sorted by newest.
     */
    public ArrayList<Notification> getNotifications(){
        ArrayList<Notification> notifications = new ArrayList<Notification>();

        SQLiteDatabase db = this.getReadableDatabase();
        String query =
                "select * from " + NOTIFICATIONS_TABLE + " ORDER BY " + NOTIF_TIMESTAMP + " DESC";
        Cursor cursor = db.rawQuery(query, null);

        int idIndex = cursor.getColumnIndex(NOTIF_ID);
        int messageIndex = cursor.getColumnIndex(NOTIF_MESSAGE);
        int timestampIndex = cursor.getColumnIndex(NOTIF_TIMESTAMP);
        int disclosedIndex = cursor.getColumnIndex(NOTIF_DISCLOSED);

        if(cursor.moveToFirst()) {
            do {

                Notification notification =  new Notification(
                        cursor.getInt(idIndex),
                        cursor.getString(messageIndex),
                        cursor.getString(timestampIndex),
                        cursor.getInt(disclosedIndex)==1
                );

                notifications.add(notification);


            } while (cursor.moveToNext());
            cursor.close();
        }
        db.close();

        return notifications;
    }
}
