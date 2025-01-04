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

/**
 * CameraActivity is responsible for displaying a live feed from a camera using a WebView.
 * It includes a progress bar for loading feedback, a button to navigate back to the previous screen,
 * and error handling mechanisms to display appropriate messages when the feed fails to load.
 */
public class CameraActivity extends AppCompatActivity {

    // UI components
    ProgressBar superProgressBar;
    ImageView superImageView;
    WebView superWebView;

    // Constants
    private static final String CAMERA_URL = "http://192.168.11.8:8000"; // Camera feed URL
    private static final int TIMEOUT_MS = 10000; // Timeout duration in milliseconds
    private boolean isPageLoaded = false; // Tracks whether the page has successfully loaded

    /**
     * Called when the activity is first created.
     * Initializes the UI components, sets up the WebView, and handles the Go Back button functionality.
     *
     * @param savedInstanceState If the activity is being re-initialized after previously being shut down,
     *                           this Bundle contains the most recent data supplied by onSaveInstanceState.
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        // Initialize UI components
        superProgressBar = findViewById(R.id.myProgressBar);
        superImageView = findViewById(R.id.myImageView);
        superWebView = findViewById(R.id.myWebView);

        // Initialize the Go Back button
        Button goBackButton = findViewById(R.id.goBackButton);
        goBackButton.setOnClickListener(v -> {
            // Finish the activity to return to the previous screen
            finish();
        });

        // Configure WebView settings
        superProgressBar.setMax(100);
        superWebView.getSettings().setJavaScriptEnabled(true);
        superWebView.getSettings().setLoadWithOverviewMode(true);
        superWebView.getSettings().setUseWideViewPort(true);
        superWebView.setScrollBarStyle(WebView.SCROLLBARS_OUTSIDE_OVERLAY);
        superWebView.setScrollbarFadingEnabled(true);

        // Set WebViewClient to handle loading and errors
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

        // Set WebChromeClient to handle progress updates and title changes
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

        // Start loading the camera feed
        superWebView.loadUrl(CAMERA_URL);

        // Set up a timeout to handle cases where the page doesn't load
        new Handler().postDelayed(() -> {
            if (!isPageLoaded) {
                showError();
            }
        }, TIMEOUT_MS);
    }

    /**
     * Displays an error message and loads an error HTML page in the WebView.
     * Called when the camera feed fails to load within the specified timeout or encounters an error.
     */
    private void showError() {
        // Stop loading the page and display an error message
        superWebView.stopLoading();
        String errorHtml = "<html><body style='text-align:center; font-size:20px; color:red;'><h1>Couldn't connect to camera</h1><p>Please check your connection or try again later.</p></body></html>";
        superWebView.loadData(errorHtml, "text/html", "UTF-8");

        // Show a toast message for immediate feedback
        Toast.makeText(this, "Failed to connect to the camera", Toast.LENGTH_LONG).show();
    }

    /**
     * Handles the back button press.
     * If the WebView can go back in its history, it navigates back. Otherwise, it finishes the activity.
     */
    @Override
    public void onBackPressed() {
        if (superWebView.canGoBack()) {
            superWebView.goBack();
        } else {
            finish();
        }
    }
}
