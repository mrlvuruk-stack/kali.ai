[Setup]
AppName=Kali AI
AppVersion=1.0.0
DefaultDirName={localappdata}\Kali AI
DefaultGroupName=Kali AI
OutputDir=setup
OutputBaseFilename=Kali_Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=compiler:SetupClassicIcon.ico
UninstallDisplayIcon={app}\Kali.exe
WizardStyle=modern

[Files]
Source: "dist\Kali.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "app.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "database.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "ingest.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Kali AI"; Filename: "{app}\Kali.exe"
Name: "{autodesktop}\Kali AI"; Filename: "{app}\Kali.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\Kali.exe"; Description: "Launch Kali AI"; Flags: nowait postinstall skipifsilent
