package com.example.childsafetyapplication;

import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class NotificationsActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private NotificationsAdapter adapter;
    private DBHelper dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notifications);

        dbHelper = new DBHelper(this);
        recyclerView = findViewById(R.id.recyclerViewNotifications);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        loadNotifications();
    }

    private void loadNotifications() {
        ArrayList<Notification> notifications = dbHelper.getNotifications();
        adapter = new NotificationsAdapter(notifications, dbHelper, notification -> {
            dbHelper.discloseNotifications(notification.getId());
            Toast.makeText(this, "Notification disclosed!", Toast.LENGTH_SHORT).show();
            loadNotifications(); // Refresh the list
        });
        recyclerView.setAdapter(adapter);
    }
}