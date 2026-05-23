# ✺ Kali AI (Kali.ai)
> **The Ultimate Private Local AI Desktop Assistant & Conversational Loot Crate Architect**

[![GitHub License](https://img.shields.io/github/license/mrlvuruk-stack/kali.ai?style=flat-square&color=blue)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![React Version](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Gemini Engine](https://img.shields.io/badge/Gemini-3.5%20Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Ollama Integration](https://img.shields.io/badge/Ollama-Local-000000?style=flat-square&logo=cpu)](https://ollama.com/)

Kali is a completely private, locally-hosted, agentic AI desktop assistant and Android companion. With **Version 2.0**, Kali introduces a stunning, glassmorphic **React Web UI** and the **Loot Crate (DocBFF)** system — a conversational AI product architect that designs full project blueprints (PRD + TRD + DRD + QA specs) just by chatting with you like a friend.

---

## 📐 Architecture & Components (Detailed Breakdown)

```mermaid
graph TD
    User([User]) <--> |Interacts| ReactApp[Vite React Frontend<br>Port 5173]
    AndroidApp[Android Companion App<br>Jetpack Compose WebView] <--> |Connects| ReactApp
    
    subgraph backend ["Kali Core Services"]
        ReactApp <--> |Local API| Ollama[Ollama Local LLM<br>llama3.2 / mistral]
        ReactApp <--> |Cloud API (Optional)| Gemini[Gemini 3.5 Flash API]
        ReactApp <--> |Data Store| SQLite[(SQLite Database)]
        
        ReactApp <--> PyBackend[Streamlit Python Backend<br>Port 8501]
        PyBackend <--> Agent[ReAct Agent Executor]
        Agent <--> Tools[System Control Tools]
    end
```

### 1. 🎨 The Interactive Frontend Layer (`kali-frontend/`)
Built with React, Vite, and glassmorphic Vanilla CSS. It provides a visual interface for managing AI sessions, projects, settings, and documents.

*   **`src/App.jsx` (Main Shell Orchestrator)**:
    Handles core state management for the active project, current conversation session, active panel view mode (`chat` vs. `lootcrate`), and coordinates sidebar open/closed status.
*   **`src/components/Sidebar.jsx`**:
    Displays active projects and sessions with dynamic HSL-generated color coding. Integrates mode selectors and live system status indicator badges (Ollama/Gemini state).
*   **`src/components/Header.jsx`**:
    Provides navigation paths, workspace indicators, sidebar toggle controllers, and active model tag badges.
*   **`src/components/ChatArea.jsx`**:
    Directs standard Hinglish dialog flow, watches for documentation triggers (auto-detection), appends visual notification nudges, and keeps conversation lists synchronised.
*   **`src/components/LootCratePanel.jsx`**:
    A specialized workspace to generate full documentation packages. Displays a progress loader (*Drafting*, *Polishing*, *Formatting*), houses PRD/TRD/DRD/QA document preview tabs, and mounts markdown file export downloads.
*   **`src/components/ChatBubble.jsx`**:
    Renders styled chat logs using gradient bubbles for the user, frosted cards for the AI, and mounts quick-action routing triggers inside system nudges.
*   **`src/components/InputBar.jsx`**:
    Houses the modern chat input bar, locking dynamically when the system is processing a request.
*   **`src/components/WelcomeScreen.jsx`**:
    Greets the user with a pulsing gradient logo and mounts clickable suggested project starter cards.
*   **`src/services/geminiService.js`**:
    Direct client-side connector to Google's Gemini API utilizing the custom Developer Key. Orchestrates model inputs and parses standard structured string dividers automatically.
*   **`src/config.js`**:
    Stores environment parameters like target models, API keys, and local server base ports.

---

### 2. 🧠 Local AI Model Orchestration (Ollama)
Handles privacy-first offline interactions, quick drafts, and general assistant fallback routines.

*   **Local Host Port (`localhost:11434`)**:
    Exposes Ollama's REST interface to local callers.
*   **Target Core Models**:
    *   `llama3.2` (Default local model): Optimal balance of memory usage and speed on consumer laptops.
    *   `mistral`: Fallback choice for extended context sizes and structural JSON outputs.
*   **Instant Draft Generation**:
    Processes conversational summaries locally before formatting structures are forwarded.

---

### 3. ⚡ High-Performance Refiner Layer (Gemini)
Performs advanced semantic engineering and builds deep documentation frameworks.

*   **Google Gemini API (`v1beta` Endpoint)**:
    Accesses Google's global models directly with sub-second execution speeds.
*   **Primary Active Model (`gemini-3.5-flash`)**:
    Leverages high-speed context compilation to polish raw local Ollama drafts into pristine, formatted technical files.
*   **Secure API Bindings**:
    Operates strictly via client-side fetch, ensuring keys are restricted to local machines.

---

### 4. 🐍 Python Core & Agent Execution Layer (`Kali--main/`)
Operates as the desktop controller, code running environment, and RAG document processor.

*   **`app.py` (Main Python Backend)**:
    Coordinates Python service loops, launches local tool registries, routes categories (DOCS/WEB/CHAT) via a routing chain, and operates a LangChain ReAct executor.
*   **`database.py` (Persistent Schema Manager)**:
    Manages local SQLite database operations, establishing tables for:
    *   `projects`: Groups workspace items.
    *   `sessions`: Manages historical timelines.
    *   `messages`: Logs persistent text history.
    *   `artifacts`: References local charts, media, and images.
    *   `settings`: Secure local store for LLM temperature and models.
*   **`ingest.py` (Local Vector Store Processor)**:
    Leverages `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`) to chunk, vectorize, and persist local PDF documents into a local `Chroma` database for instant semantic search.
*   **`launcher.py` / `build.py` / `installer.iss`**:
    Coordinates executable compilation, folder bindings, and native OS installers.

---

### 5. 🛠️ Agent PC Control Toolkit (LangChain & Classic Tools)
Enables Kali to execute actions directly on the user's PC when requested.

*   **Windows Application Auto-Launcher (`launch_windows_application`)**:
    Scans the system's local Start Menu directories to locate and launch desktop applications (e.g. OBS, VS Code) on voice/text request.
*   **Python REPL Execution Sandbox (`PythonREPLTool`)**:
    Compiles and runs Python code locally. When data graphs or plots are requested, it outputs them as a local file (`chart.png`) and embeds them directly into the UI.
*   **System Command Shell (`ShellTool`)**:
    Gives the local AI ReAct executor authorization to run administrative commands safely within the OS shell environment.
*   **Unified File Management (`FileManagementToolkit`)**:
    Allows Kali to create, read, update, delete, and copy local project files.

---

### 6. 📱 Mobile Companion Layer (`kali-android/`)
Extends desktop power straight to your mobile device.

*   **Jetpack Compose WebView Engine**:
    Provides a fast, hardware-accelerated wrapper to display the React workspace on mobile screens.
*   **Host Auto-Resolution**:
    Automatically maps requests to the computer's active local IP address, ensuring seamless sync on local Wi-Fi networks.
*   **Pre-compiled Delivery (`Kali-AI.apk`)**:
    Ready-to-install Android package for direct sideloading.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Node.js** (v18+) & **Python 3.8+**
- **Ollama** installed locally. Make sure you pull your desired model:
  ```bash
  ollama pull llama3.2
  ```

---

### 2. Running the React Frontend

1. Navigate to the frontend directory:
   ```bash
   cd kali-frontend
   ```
2. Configure your keys:
   - Rename `src/config.example.js` to `src/config.js`.
   - Add your Gemini API key:
     ```javascript
     export const GEMINI_API_KEY = "AIzaSy...";
     ```
3. Install packages and start Vite dev server:
   ```bash
   npm install
   npm run dev
   ```
4. Open [http://localhost:5173/](http://localhost:5173/) in your browser.

---

### 3. Running the Python Backend Agent

1. Navigate to the backend directory:
   ```bash
   cd Kali--main
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the vector store (if using Document Reader):
   ```bash
   python ingest.py
   ```
4. Start the Streamlit application:
   ```bash
   python -m streamlit run app.py
   ```

---

## 🛡️ Security & Privacy
- **Direct Client-to-API Calls**: Your Gemini API key is stored locally in `src/config.js` (which is in `.gitignore`) and is never sent to any external server.
- **Local SQLite Storage**: Your chat history, session records, and generated documents are saved on your own machine.

---
*Created with love by mrlv. Build beautifully, ship securely.* 🚀
