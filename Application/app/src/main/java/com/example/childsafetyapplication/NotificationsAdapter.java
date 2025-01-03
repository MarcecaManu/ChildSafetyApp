package com.example.childsafetyapplication;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class NotificationsAdapter extends RecyclerView.Adapter<NotificationsAdapter.ViewHolder> {

    private ArrayList<Notification> notifications;
    private OnNotificationClickListener listener;
    private DBHelper dbHelper;

    public interface OnNotificationClickListener {
        void onNotificationClick(Notification notification);
    }

    public NotificationsAdapter(ArrayList<Notification> notifications, DBHelper dbHelper, OnNotificationClickListener listener) {
        this.notifications = notifications;
        this.listener = listener;
        this.dbHelper = dbHelper;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(android.R.layout.simple_list_item_2, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Notification notification = notifications.get(position);
        holder.messageTextView.setText(notification.getMessage());
        holder.timestampTextView.setText(notification.getTimestamp());

        if (notification.isDisclosed()) {
            holder.itemView.setAlpha(0.5f); // Mark as disclosed (visually distinct)
        } else {
            holder.itemView.setAlpha(1.0f);
        }

        holder.itemView.setOnClickListener(v -> listener.onNotificationClick(notification));
    }

    @Override
    public int getItemCount() {
        return notifications.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {

        TextView messageTextView;
        TextView timestampTextView;

        ViewHolder(View itemView) {
            super(itemView);
            messageTextView = itemView.findViewById(android.R.id.text1);
            timestampTextView = itemView.findViewById(android.R.id.text2);
        }
    }
}