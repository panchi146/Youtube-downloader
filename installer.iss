#define MyAppName "YouTube Downloader"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Panchi"
#define MyAppExeName "YouTube Downloader.exe"

[Setup]
AppId={{F4D8C5F6-9D9A-4A4B-8A12-YOUTUBE-DOWNLOADER}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer_output
OutputBaseFilename=YouTube_Downloader_Setup
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Tạo biểu tượng ngoài Desktop"; GroupDescription: "Tùy chọn:"; Flags: unchecked

[Files]
Source: "dist\YouTube Downloader\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Mở {#MyAppName}"; Flags: nowait postinstall skipifsilent