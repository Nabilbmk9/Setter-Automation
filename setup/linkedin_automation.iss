; Script généré par Inno Setup Compiler
[Setup]
; Informations de base
AppName=LinkedIn Automation Bot
AppVersion=1.0
DefaultDirName={userappdata}\LinkedInAutomationBot
DefaultGroupName=LinkedIn Automation Bot
OutputDir=.\output
OutputBaseFilename=LinkedInAutomationBotInstaller_v1
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\boulm\Python_file\setting_automation\ui\resources\logo3d.ico

[Files]
; Inclure tous les fichiers nécessaires depuis le dossier dist
Source: "C:\Users\boulm\Python_file\setting_automation\build\windows\dist\linkedin_automation\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\boulm\Python_file\setting_automation\ui\resources\logo3d.ico"; DestDir: "{app}\resources"; Flags: ignoreversion


[Icons]
; Créer un raccourci sur le bureau et dans le menu démarrer avec ton icône
Name: "{group}\LinkedIn Automation Bot"; Filename: "{app}\linkedin_automation.exe"; IconFilename: "{app}\resources\logo3d.ico"
Name: "{commondesktop}\LinkedIn Automation Bot"; Filename: "{app}\linkedin_automation.exe"; IconFilename: "{app}\resources\logo3d.ico"

[Run]
; Lancer l'application après l'installation
Filename: "{app}\linkedin_automation.exe"; Description: "{cm:LaunchProgram,LinkedIn Automation Bot}"; Flags: nowait postinstall skipifsilent
