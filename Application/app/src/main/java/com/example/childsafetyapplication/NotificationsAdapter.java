package com.example.childsafetyapplication;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

/**
 * Adapter class for managing and displaying a list of notifications in a RecyclerView.
 * Each notification contains a message, a timestamp, and a disclosed status.
 */
public class NotificationsAdapter extends RecyclerView.Adapter<NotificationsAdapter.ViewHolder> {

    private ArrayList<Notification> notifications; // List of notifications to display
    private OnNotificationClickListener listener; // Listener for handling click events on notifications
    private DBHelper dbHelper; // Helper for database interactions

    /**
     * Interface for handling click events on individual notifications.
     */
    public interface OnNotificationClickListener {
        /**
         * Triggered when a notification item is clicked.
         *
         * @param notification The clicked notification.
         */
        void onNotificationClick(Notification notification);
    }

    /**
     * Constructor for NotificationsAdapter.
     *
     * @param notifications List of notifications to display in the RecyclerView.
     * @param dbHelper      Database helper for managing notifications.
     * @param listener      Listener for handling notification click events.
     */
    public NotificationsAdapter(ArrayList<Notification> notifications, DBHelper dbHelper, OnNotificationClickListener listener) {
        this.notifications = notifications;
        this.listener = listener;
        this.dbHelper = dbHelper;
    }

    /**
     * Inflates the layout for each notification item.
     *
     * @param parent   The parent ViewGroup into which the new View will be added.
     * @param viewType The view type of the new View.
     * @return A new ViewHolder containing the inflated View.
     */
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(android.R.layout.simple_list_item_2, parent, false);
        return new ViewHolder(view);
    }

    /**
     * Binds the data of a notification to the corresponding ViewHolder.
     *
     * @param holder   The ViewHolder containing the Views to bind data to.
     * @param position The position of the notification in the list.
     */
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Notification notification = notifications.get(position);
        holder.messageTextView.setText(notification.getMessage());
        holder.timestampTextView.setText(notification.getTimestamp());

        // Visually distinguish disclosed notifications
        if (notification.isDisclosed()) {
            holder.itemView.setAlpha(0.5f);
        } else {
            holder.itemView.setAlpha(1.0f);
        }

        // Set a click listener for the notification item
        holder.itemView.setOnClickListener(v -> listener.onNotificationClick(notification));
    }

    /**
     * Returns the total number of notifications in the list.
     *
     * @return The number of notifications.
     */
    @Override
    public int getItemCount() {
        return notifications.size();
    }

    /**
     * ViewHolder class for holding the Views of a single notification item.
     */
    static class ViewHolder extends RecyclerView.ViewHolder {

        TextView messageTextView; // TextView for the notification message
        TextView timestampTextView; // TextView for the notification timestamp

        /**
         * Constructor for ViewHolder.
         *
         * @param itemView The View representing a single notification item.
         */
        ViewHolder(View itemView) {
            super(itemView);
            messageTextView = itemView.findViewById(android.R.id.text1);
            timestampTextView = itemView.findViewById(android.R.id.text2);
        }
    }
}
