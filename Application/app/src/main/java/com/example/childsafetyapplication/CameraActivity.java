package com.example.childsafetyapplication;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Handler;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class CameraActivity extends AppCompatActivity {

    ProgressBar superProgressBar;
    ImageView superImageView;
    WebView superWebView;

    private static final String CAMERA_URL = "http://192.168.11.8:8000";
    private static final int TIMEOUT_MS = 10000; // 10 seconds
    private boolean isPageLoaded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        superProgressBar = findViewById(R.id.myProgressBar);
        superImageView = findViewById(R.id.myImageView);
        superWebView = findViewById(R.id.myWebView);

        // Initialize the Go Back button
        Button goBackButton = findViewById(R.id.goBackButton);
        goBackButton.setOnClickListener(v -> {
            // Simply finish the activity to go back to the previous one
            finish(); // This pops CameraActivity from the stack and goes back to MainActivity or the calling activity
        });

        // Remaining setup code for WebView, ProgressBar, etc.
        superProgressBar.setMax(100);
        superWebView.getSettings().setJavaScriptEnabled(true);
        superWebView.getSettings().setLoadWithOverviewMode(true);
        superWebView.getSettings().setUseWideViewPort(true);
        superWebView.setScrollBarStyle(WebView.SCROLLBARS_OUTSIDE_OVERLAY);
        superWebView.setScrollbarFadingEnabled(true);

        // Set WebViewClient to handle errors
        superWebView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                isPageLoaded = true; // Page loaded successfully
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                super.onReceivedError(view, request, error);
                showError();
            }
        });

        // Set WebChromeClient for progress and title
        superWebView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                super.onProgressChanged(view, newProgress);
                superProgressBar.setProgress(newProgress);
            }

            @Override
            public void onReceivedTitle(WebView view, String title) {
                super.onReceivedTitle(view, title);
                if (getSupportActionBar() != null) {
                    getSupportActionBar().setTitle(title);
                }
            }

            @Override
            public void onReceivedIcon(WebView view, Bitmap icon) {
                super.onReceivedIcon(view, icon);
                superImageView.setImageBitmap(icon);
            }
        });

        // Start loading the page
        superWebView.loadUrl(CAMERA_URL);

        // Set up a timeout handler
        new Handler().postDelayed(() -> {
            if (!isPageLoaded) {
                showError();
            }
        }, TIMEOUT_MS);
    }

    private void showError() {
        // Stop loading the page and display an error
        superWebView.stopLoading();
        String errorHtml = "<html><body style='text-align:center; font-size:20px; color:red;'><h1>Couldn't connect to camera</h1><p>Please check your connection or try again later.</p></body></html>";
        superWebView.loadData(errorHtml, "text/html", "UTF-8");

        // Optionally show a toast for immediate feedback
        Toast.makeText(this, "Failed to connect to the camera", Toast.LENGTH_LONG).show();
    }

    @Override
    public void onBackPressed() {
        if (superWebView.canGoBack()) {
            superWebView.goBack();
        } else {
            finish();
        }
    }
}
