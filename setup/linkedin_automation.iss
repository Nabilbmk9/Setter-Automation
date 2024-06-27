; Script généré par Inno Setup Compiler
[Setup]
; Informations de base
AppName=LinkedIn Automation Bot
AppVersion=1.0
DefaultDirName={pf}\LinkedInAutomationBot
DefaultGroupName=LinkedIn Automation Bot
OutputDir=.\output
OutputBaseFilename=LinkedInAutomationBotInstaller
Compression=lzma
SolidCompression=yes

[Files]
; Inclure tous les fichiers nécessaires depuis le dossier dist
Source: "C:\Users\boulm\Python_file\setting_automation\build\windows\dist\linkedin_automation\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Créer un raccourci sur le bureau et dans le menu démarrer
Name: "{group}\LinkedIn Automation Bot"; Filename: "{app}\linkedin_automation.exe"
Name: "{commondesktop}\LinkedIn Automation Bot"; Filename: "{app}\linkedin_automation.exe"

[Run]
; Lancer l'application après l'installation
Filename: "{app}\linkedin_automation.exe"; Description: "{cm:LaunchProgram,LinkedIn Automation Bot}"; Flags: nowait postinstall skipifsilent
