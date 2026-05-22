import os
import sys
import subprocess
import urllib.request
import time
import shutil
import tkinter as tk
from tkinter import ttk
import threading

class KaliLauncher:
    def __init__(self):
        # Create a sleek, dark-mode splash screen
        self.root = tk.Tk()
        self.root.title("Kali AI - Bootstrapper")
        self.root.geometry("450x160")
        self.root.resizable(False, False)
        self.root.configure(bg="#18181A")
        
        # Remove standard window borders for a modern look (optional, but clean)
        self.root.overrideredirect(True)

        # Center the window on screen
        window_width = 450
        window_height = 160
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        # Title Label
        self.title_label = tk.Label(self.root, text="✺ Kali AI", fg="#E8E5DF", bg="#18181A", font=("Georgia", 18))
        self.title_label.pack(pady=(20, 5))

        # Status Label
        self.label = tk.Label(self.root, text="Initializing environment...", fg="gray", bg="#18181A", font=("Helvetica", 10))
        self.label.pack(pady=5)

        # Progress Bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", thickness=8, background="#4CAF50", troughcolor="#2D2D2D", bordercolor="#18181A")
        
        self.progress = ttk.Progressbar(self.root, style="TProgressbar", orient="horizontal", length=350, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start(15)

    def update_text(self, text):
        self.label.config(text=text)
        self.root.update()

    def get_ollama_path(self):
        path = shutil.which("ollama")
        if path: return path
        
        # Check standard Windows installation directory
        local_app_data = os.environ.get('LOCALAPPDATA', '')
        default_path = os.path.join(local_app_data, 'Programs', 'Ollama', 'ollama.exe')
        if os.path.exists(default_path):
            return default_path
        return None

    def run_checks(self):
        try:
            # 1. Check for Ollama
            self.update_text("Checking for Ollama Engine...")
            time.sleep(1) # Fake delay for UI smoothness
            ollama_path = self.get_ollama_path()
            
            if not ollama_path:
                self.update_text("Ollama not found. Downloading installer (may take a moment)...")
                installer_path = os.path.join(os.environ.get('TEMP', 'C:\\temp'), "OllamaSetup.exe")
                
                # Create temp dir if it doesn't exist
                os.makedirs(os.path.dirname(installer_path), exist_ok=True)
                urllib.request.urlretrieve("https://ollama.com/download/OllamaSetup.exe", installer_path)
                
                self.update_text("Running Ollama Setup... Please complete the installation.")
                # Run the installer and wait for it to finish
                subprocess.run([installer_path], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                self.update_text("Waiting for Ollama background service to start...")
                time.sleep(5)
                ollama_path = self.get_ollama_path()
            
            if not ollama_path:
                raise Exception("Ollama installation failed or path not found.")

            # 2. Check for Llama 3.2 model
            self.update_text("Verifying AI Neural Weights (Llama 3.2)...")
            result = subprocess.run([ollama_path, "list"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            if "llama3.2" not in result.stdout:
                self.update_text("Downloading Llama 3.2 (2.0GB)... This will take a while.")
                # We run this, it will block until download completes
                subprocess.run([ollama_path, "pull", "llama3.2"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # 3. Launch the Streamlit App
            self.update_text("Launch Sequence Initiated. Starting Kali UI...")
            time.sleep(1)
            self.root.after(100, self.launch_streamlit)
            
        except Exception as e:
            with open("error.log", "w") as f:
                import traceback
                f.write(traceback.format_exc())
            self.update_text(f"Critical Error: {str(e)}")
            self.progress.stop()
            # Give user 5 seconds to read the error before closing
            time.sleep(5)
            self.root.destroy()

    def launch_streamlit(self):
        try:
            # Resolve the true base directory whether running as script or .exe
            base_dir = os.path.dirname(os.path.abspath(sys.executable))
            if "python" in sys.executable.lower():
                base_dir = os.path.dirname(os.path.abspath(__file__))
                
            # If Kali.exe was launched from inside the 'dist' folder, move up one directory
            if os.path.basename(base_dir).lower() == "dist":
                base_dir = os.path.dirname(base_dir)
                
            streamlit_path = os.path.join(base_dir, "venv", "Scripts", "streamlit.exe")
            app_path = os.path.join(base_dir, "app.py")
            
            if not os.path.exists(streamlit_path):
                self.update_text("Building Virtual Environment (Downloading 1.5GB of AI Tools)...")
                self.root.update()
                try:
                    subprocess.run(["python", "-V"], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                except (FileNotFoundError, subprocess.CalledProcessError):
                    self.update_text("Python not found! Installing Python via Winget...")
                    self.root.update()
                    subprocess.run(["winget", "install", "-e", "--id", "Python.Python.3.11", "--silent", "--accept-package-agreements", "--accept-source-agreements"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    time.sleep(3)
                    
                subprocess.run(["python", "-m", "venv", "venv"], check=True, cwd=base_dir, creationflags=subprocess.CREATE_NO_WINDOW)
                pip_path = os.path.join(base_dir, "venv", "Scripts", "pip.exe")
                self.update_text("Installing Langchain & Streamlit...")
                self.root.update()
                subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True, cwd=base_dir, creationflags=subprocess.CREATE_NO_WINDOW)
                
                # If it still didn't install correctly, fallback to system path
                if not os.path.exists(streamlit_path):
                    streamlit_path = shutil.which("streamlit")
                    if not streamlit_path:
                        raise FileNotFoundError(f"Could not find streamlit! Make sure Kali.exe is in the project folder.")
            else:
                # If venv exists, silently ensure any new requirements are installed
                pip_path = os.path.join(base_dir, "venv", "Scripts", "pip.exe")
                try:
                    subprocess.run([pip_path, "install", "-r", "requirements.txt", "--quiet"], cwd=base_dir, timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
                except Exception:
                    pass
            
            subprocess.Popen([streamlit_path, "run", app_path], cwd=base_dir, creationflags=subprocess.CREATE_NO_WINDOW)
            self.root.destroy()
            
        except Exception as e:
            import tkinter.messagebox
            # Show the error before dying so it's not silent
            self.root.withdraw() 
            tkinter.messagebox.showerror("Kali AI - Launch Error", str(e))
            self.root.destroy()

def main():
    launcher = KaliLauncher()
    # Run the heavy checks in a background thread so the UI progress bar doesn't freeze
    threading.Thread(target=launcher.run_checks, daemon=True).start()
    launcher.root.mainloop()

if __name__ == "__main__":
    main()
