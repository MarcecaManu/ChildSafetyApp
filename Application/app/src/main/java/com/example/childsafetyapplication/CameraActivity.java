package com.example.childsafetyapplication;

import android.os.Bundle;
import android.widget.VideoView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import android.widget.VideoView;

public class CameraActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_camera);

        VideoView videoView = findViewById(R.id.videoView);

        // Replace with the RTSP/HTTP URL of the camera stream
        String streamUrl = "rtsp://1701954d6d07.entrypoint.cloud.wowza.com:1935/app-m75436g0/27122ffc_stream2";
        videoView.setVideoPath(streamUrl);

        videoView.setOnPreparedListener(mediaPlayer -> mediaPlayer.setLooping(false));
        videoView.start();
    }
}