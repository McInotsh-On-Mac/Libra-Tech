[Setup]
AppName=LibraTech Sentiment Analysis
AppVersion=1.0
DefaultDirName={pf}\LibraTech
DefaultGroupName=LibraTech
OutputDir=dist
OutputBaseFilename=LibraTechInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\LibraTech.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".env"; DestDir: "{app}"; Flags: onlyifdoesntexist
Source: "README.md"; DestDir: "{app}"

[Icons]
Name: "{group}\LibraTech"; Filename: "{app}\LibraTech.exe"
Name: "{commondesktop}\LibraTech"; Filename: "{app}\LibraTech.exe"

[Run]
Filename: "{app}\LibraTech.exe"; Description: "Launch LibraTech"; Flags: nowait postinstall skipifsilent
