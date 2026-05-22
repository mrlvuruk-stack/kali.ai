import os
import sys
import subprocess
import shutil

def run_cmd(cmd, check=True):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check)
    return result

def main():
    print("Kali AI - Build & Package Automation")
    print("=======================================")
    
    # 1. Ensure PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        run_cmd([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 2. Compile launcher.py into dist/Kali.exe
    print("\nCompiling launcher.py into Kali.exe...")
    build_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name=Kali",
        "--clean",
        "launcher.py"
    ]
    run_cmd(build_cmd)
    
    print("\nLauncher compiled successfully at: dist\\Kali.exe")
    
    # 3. Compile Inno Setup Installer if available
    print("\nLooking for Inno Setup compiler (ISCC.exe)...")
    iscc_path = shutil.which("iscc")
    if not iscc_path:
        # Check default installation directories
        default_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe"
        ]
        for p in default_paths:
            if os.path.exists(p):
                iscc_path = p
                break
                
    if iscc_path:
        print(f"Found Inno Setup at: {iscc_path}")
        print("Compiling installer.iss...")
        try:
            run_cmd([iscc_path, "installer.iss"])
            print("\nSetup package created successfully at: setup\\Kali_Setup.exe")
        except Exception as e:
            print(f"Error compiling installer: {e}")
    else:
        print("Inno Setup (ISCC.exe) not found on PATH or in standard paths.")
        print("To generate the installer setup package:")
        print("1. Download and install Inno Setup 6 (https://jrsoftware.org/isdl.php)")
        print("2. Open Inno Setup Compiler, load 'installer.iss' and compile it.")
        print("Alternatively, you can distribute the files in the directory along with dist\\Kali.exe.")

if __name__ == "__main__":
    main()
