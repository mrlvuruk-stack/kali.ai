# ✺ Kali AI (Kali.ai)

[![GitHub License](https://img.shields.io/github/license/mrlvuruk-stack/kali.ai?style=flat-square&color=blue)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Android Comp](https://img.shields.io/badge/Android-Companion-3DDC84?style=flat-square&logo=android&logoColor=white)](./kali-android)

Kali is a completely private, locally-hosted, agentic AI desktop assistant and Android companion. Unlike cloud-based LLM services, Kali runs 100% on your own hardware using Ollama. No data is ever sent to the cloud, and she can natively interact with your computer!

---

## 📐 Architecture & Components

The workspace is organized into four main layers:

```mermaid
graph TD
    User([User]) <--> |Interacts| WebApp[Streamlit Web UI<br>Port 8501]
    AndroidApp[Android Companion App<br>Jetpack Compose WebView] <--> |Connects via Local IP| WebApp
    
    subgraph Python Backend (Streamlit App)
        WebApp <--> Agent[ReAct Agent Executor]
        WebApp <--> DB[(SQLite Memory Database)]
        
        Agent <--> Ollama[Ollama Local LLM]
        Agent <--> Tools[Agent Tools]
        
        subgraph Tools
            WinApp[Native App Launcher]
            PyInterpreter[Python Code Interpreter]
            RAG[Chroma DB / PDF Document Reader]
            Search[DuckDuckGo Web Search]
        end
    end
```

| Component | Path / File | Description |
| :--- | :--- | :--- |
| **Python Backend** | [Kali--main/](file:///c:/Users/MR%20LV/Downloads/Kali--main/Kali--main) | Streamlit web interface, SQLite database manager, and LangChain ReAct agent backend. |
| **Android Wrapper** | [kali-android/](file:///c:/Users/MR%20LV/Downloads/Kali--main/kali-android) | Jetpack Compose WebView companion wrapper app. |
| **Pre-built Release** | [Kali-AI.apk](file:///c:/Users/MR%20LV/Downloads/Kali--main/Kali-AI.apk) | Installer package for direct Android deployment. |
| **CLI Installer** | [install.cmd](file:///c:/Users/MR%20LV/Downloads/Kali--main/install.cmd) | Automated script to install and configure the Google Android CLI developer tools locally. |

---

## ✨ Features

- **100% Local & Private:** Powered by Ollama. Fully functional offline.
- **Persistent Context Memory:** Uses a structured SQLite database to organize chat histories into **Projects** and **Sessions** so you can pick up exactly where you left off.
- **Python Code Interpreter:** Generates and runs Python code locally. When creating graphs or plots, it automatically saves them and renders the image directly in your chat interface.
- **Native Windows App Launcher:** Open Windows apps directly. Ask *"Open OBS"* or *"Launch VS Code"*, and Kali will scan your Start Menu shortcuts to launch them.
- **Local PDF Document Reader (RAG):** Ingest your documents using the LangChain and Chroma vector store setup, then query them locally.
- **Web Search Integration:** Seamless fallback to DuckDuckGo search when you ask about real-time events.
- **Companion App Wrapper:** Run the workspace on your Android device locally inside a native web view.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.8+** (with "Add to PATH" checked).
- **Ollama** installed locally. Make sure you pull a model (e.g., `llama3` or `llama3.2`):
  ```bash
  ollama pull llama3.2
  ```

---

### 2. Running the Desktop Application (Python Backend)

1. Navigate to the Python backend directory:
   ```bash
   cd Kali--main
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the vector store database (if you plan to use Document Reader):
   ```bash
   python ingest.py
   ```
4. Run the Streamlit application:
   ```bash
   python -m streamlit run app.py
   ```
5. A browser window will automatically open at `http://localhost:8501`.

---

### 3. Setting Up the Android Companion App

The Android app is a custom Jetpack Compose application designed to wrap the Streamlit web app in a WebView.

#### Option A: Install Pre-built APK
Copy the [Kali-AI.apk](file:///c:/Users/MR%20LV/Downloads/Kali--main/Kali-AI.apk) to your Android device and install it directly.

#### Option B: Build and Customize the App
1. Open the [kali-android/](file:///c:/Users/MR%20LV/Downloads/Kali--main/kali-android) directory in Android Studio.
2. In [MainActivity.kt](file:///c:/Users/MR%20LV/Downloads/Kali--main/kali-android/app/src/main/java/com/example/kaliai/MainActivity.kt#L40), update the URL to your computer's local IP address (instead of `http://10.125.137.179:8501`):
   ```kotlin
   loadUrl("http://<YOUR_LOCAL_IP>:8501")
   ```
3. Run the project in Android Studio or compile it to a new APK.

#### Developer CLI Environment Setup
Run the [install.cmd](file:///c:/Users/MR%20LV/Downloads/Kali--main/install.cmd) script in your terminal to automatically download, install, and add Google's developer `android` CLI tool to your system's path variables.

---

## 🛠️ Configuration & Settings

Inside the Streamlit workspace, click on the **⚙️ Settings** expander in the sidebar to configure:
- **LLM Model**: Define which Ollama model you want Kali to use (defaults to `llama3.2`).
- **Temperature**: Control LLM creativity (defaults to `0.2`).
- **Code Interpreter Mode**: Toggle the computer-controlling ReAct agent execution model.
