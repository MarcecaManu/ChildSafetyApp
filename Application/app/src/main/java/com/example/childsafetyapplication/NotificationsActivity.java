package com.example.childsafetyapplication;

import android.os.Bundle;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

/**
 * Activity for displaying and managing a list of notifications.
 * Users can view notifications and mark them as disclosed.
 */
public class NotificationsActivity extends AppCompatActivity {

    private RecyclerView recyclerView; // RecyclerView for displaying notifications
    private NotificationsAdapter adapter; // Adapter for managing notification data
    private DBHelper dbHelper; // Database helper for accessing notifications

    /**
     * Called when the activity is first created. Sets up the layout, initializes the database helper,
     * and loads notifications into the RecyclerView.
     *
     * @param savedInstanceState If the activity is being re-initialized after previously being shut down, this contains the data most recently supplied.
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notifications);

        // Initialize the Go Back button
        ImageButton goBackButton = findViewById(R.id.backArrow);
        goBackButton.setOnClickListener(v -> {
            // Finish the activity to return to the previous screen
            finish();
        });

        dbHelper = new DBHelper(this); // Initialize the database helper
        recyclerView = findViewById(R.id.recyclerViewNotifications); // Initialize the RecyclerView
        recyclerView.setLayoutManager(new LinearLayoutManager(this)); // Set a vertical layout manager for the RecyclerView

        loadNotifications(); // Load and display notifications
    }

    /**
     * Loads notifications from the database and sets up the RecyclerView adapter.
     * The adapter handles click events to mark notifications as disclosed.
     */
    private void loadNotifications() {
        // Retrieve notifications from the database
        ArrayList<Notification> notifications = dbHelper.getNotifications();

        // Set up the adapter with a click listener for each notification
        adapter = new NotificationsAdapter(notifications, dbHelper, notification -> {
            // Mark the notification as disclosed in the database
            dbHelper.discloseNotifications(notification.getId());

            // Show a confirmation message
            Toast.makeText(this, "Notification disclosed!", Toast.LENGTH_SHORT).show();

            // Refresh the list to reflect the changes
            loadNotifications();
        });

        // Attach the adapter to the RecyclerView
        recyclerView.setAdapter(adapter);
    }
}
