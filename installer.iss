; Inno Setup — baut PDF-Merger-Setup.exe aus der fertigen dist\PDF-Merger.exe.
;
;   iscc installer.iss
;
; Bewusst eine Installation *pro Benutzer* (PrivilegesRequired=lowest): sie
; landet unter %LocalAppData%, verlangt keine Administratorrechte und damit
; keine UAC-Abfrage. Fuer ein kleines Werkzeug ist das der freundlichere Weg.

#define AppName "PDF-Merger"
#define AppExeName "PDF-Merger.exe"
#define AppPublisher "PDF-Merger"
#define AppUrl "https://github.com/loltorres9/PDF_App"
; Version aus der gebauten Exe lesen, damit sie nur in pdfmerge_core.py steht.
#define AppVersion GetVersionNumbersString("dist\" + AppExeName)

[Setup]
; Diese GUID identifiziert das Programm bei Updates und Deinstallation.
; Sie darf sich nie aendern - sonst gilt eine neue Version als zweites Programm.
AppId={{8B2F41C6-6C4E-4E52-9E5D-2F1B7A0D9C34}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppUrl}
AppSupportURL={#AppUrl}/issues
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
DisableDirPage=auto
PrivilegesRequired=lowest
OutputDir=installer_out
OutputBaseFilename=PDF-Merger-Setup
SetupIconFile=app.ico
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName} {#AppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
; Aeltere Installation still ersetzen statt eine zweite danebenzustellen.
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "sendtoicon"; Description: "Eintrag im Explorer-Menue ""Senden an"" anlegen"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
; Damit lassen sich im Explorer markierte PDFs per Rechtsklick uebergeben.
Name: "{sendto}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: sendtoicon

[Registry]
; Traegt das Programm unter "Oeffnen mit" fuer PDF-Dateien ein - ohne die
; bestehende Standardanwendung anzuruehren.
Root: HKCU; Subkey: "Software\Classes\Applications\{#AppExeName}\shell\open\command"; \
    ValueType: string; ValueName: ""; ValueData: """{app}\{#AppExeName}"" ""%1"""; \
    Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Applications\{#AppExeName}"; \
    ValueType: string; ValueName: "FriendlyAppName"; ValueData: "{#AppName}"; \
    Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\.pdf\OpenWithList\{#AppExeName}"; \
    Flags: uninsdeletekey

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; \
    Flags: nowait postinstall skipifsilent
