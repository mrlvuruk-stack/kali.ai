package com.example.kaliai

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import com.example.kaliai.theme.KaliAITheme

class MainActivity : ComponentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    enableEdgeToEdge()
    setContent {
      KaliAITheme {
        var webView: WebView? by remember { mutableStateOf(null) }

        // Handle system back button to navigate back in web history if possible
        BackHandler(enabled = webView?.canGoBack() == true) {
          webView?.goBack()
        }

        AndroidView(
          factory = { context ->
            WebView(context).apply {
              settings.javaScriptEnabled = true
              settings.domStorageEnabled = true
              settings.databaseEnabled = true
              webViewClient = WebViewClient()
              loadUrl("http://10.125.137.179:8501")
              webView = this
            }
          },
          modifier = Modifier.fillMaxSize()
        )
      }
    }
  }
}
