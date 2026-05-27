package com.tracker.inspirationworkshop;
import android.annotation.SuppressLint; import android.app.Activity; import android.graphics.Bitmap; import android.os.Bundle;
import android.webkit.*; import android.webkit.WebView;
public class MainActivity extends Activity {
    private WebView webView;
    private static final String URL = "https://inspiration-workshop-app.fly.dev";
    @SuppressLint("SetJavaScriptEnabled") @Override
    protected void onCreate(Bundle s) {
        super.onCreate(s); webView = new WebView(this); setContentView(webView);
        WebSettings ws = webView.getSettings(); ws.setJavaScriptEnabled(true); ws.setDomStorageEnabled(true); ws.setAllowFileAccess(true); ws.setMediaPlaybackRequiresUserGesture(false); ws.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW); ws.setUseWideViewPort(true); ws.setLoadWithOverviewMode(true);
        webView.setWebViewClient(new WebViewClient() { @Override public boolean shouldOverrideUrlLoading(WebView v, String u) { return !u.startsWith("http"); } });
        webView.setWebChromeClient(new WebChromeClient() { @Override public void onPermissionRequest(PermissionRequest r) { r.grant(r.getResources()); } });
        webView.loadUrl(URL);
    }
    @Override public void onBackPressed() { if(webView.canGoBack()) webView.goBack(); else super.onBackPressed(); }
}
