# ✺ Kali AI Workspace

Kali is a completely private, locally hosted AI desktop assistant. Unlike ChatGPT or Claude, Kali runs 100% on your own hardware using Ollama. No data is ever sent to the cloud, and she can natively interact with your computer!

## ✨ Features
- **Local & Private:** Powered by your local PC. Works perfectly offline.
- **Persistent Memory:** Kali uses a built-in SQLite database to remember your previous conversations, grouped into Projects and Sessions. You can close the app and pick up exactly where you left off.
- **Native App Launcher:** Ask Kali to "Open OBS" or "Launch VS Code," and she will hunt down the shortcut on your PC and launch it in the background.
- **Code Interpreter:** Ask her to generate a graph, and she will write the Python code, execute it on your machine, and show you the generated image directly in the chat.
- **Document Reading:** Drop PDFs into your workspace, and Kali can read them and answer questions about them.

## 🚀 How to Run It

### Prerequisites
1. Install [Python](https://www.python.org/downloads/) (Make sure "Add to PATH" is checked during installation).
2. Install [Ollama](https://ollama.ai/) to run local AI models.

### Installation
1. Download or clone this repository to your computer.
2. Open a terminal (PowerShell or Command Prompt) inside the folder.
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python -m streamlit run app.py
   ```

A browser window will pop up automatically with the Kali Workspace interface!
