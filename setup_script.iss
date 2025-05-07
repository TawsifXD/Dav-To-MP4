[Setup]
AppName=DAV Converter
AppVersion=1.0
DefaultDirName={localappdata}\DAVConverter
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=DAVConverterSetup
Compression=lzma
SolidCompression=yes
LicenseFile=license.txt

[Files]
Source: "dist\converter.exe"; DestDir: "{app}"
Source: "ffmpeg.exe"; DestDir: "{app}"
Source: "ffprobe.exe"; DestDir: "{app}"
Source: "app_icon.ico"; DestDir: "{app}"
Source: "settings.ini"; DestDir: "{app}"; Flags: onlyifdoesntexist

[Icons]
Name: "{commonprograms}\DAV Converter"; Filename: "{app}\converter.exe"
Name: "{commondesktop}\DAV Converter"; Filename: "{app}\converter.exe"

[Run]
Filename: "{app}\converter.exe"; Description: "Run application"; Flags: postinstall nowait skipifsilent

[Code]
var
  ReadMePage, AboutPage: TWizardPage;

procedure InitializeWizard;
var
  ReadMeMemo, AboutMemo: TNewMemo;
begin
  // === ReadMe Page ===
  ReadMePage := CreateCustomPage(wpLicense, 'ReadMe', 'Please read the following:');
  ReadMeMemo := TNewMemo.Create(ReadMePage);
  ReadMeMemo.Parent := ReadMePage.Surface;
  ReadMeMemo.SetBounds(0, 0, ReadMePage.SurfaceWidth, ReadMePage.SurfaceHeight);
  ReadMeMemo.ReadOnly := True;
  ReadMeMemo.WordWrap := True;
  ReadMeMemo.ScrollBars := ssVertical;
  ReadMeMemo.Lines.Text :=
    'DAV Converter ReadMe:' + #13#10 +
    '------------------------' + #13#10 +
    '1. This software converts .dav files to .mp4 format.' + #13#10 +
    '2. You can use it for WhatsApp-friendly conversions.' + #13#10 +
    '3. Drag & drop supported. Batch conversion too.' + #13#10 +
    '4. Use responsibly.';

  // === About Page ===
  AboutPage := CreateCustomPage(ReadMePage.ID, 'About', 'About DAV Converter');
  AboutMemo := TNewMemo.Create(AboutPage);
  AboutMemo.Parent := AboutPage.Surface;
  AboutMemo.SetBounds(0, 0, AboutPage.SurfaceWidth, AboutPage.SurfaceHeight);
  AboutMemo.ReadOnly := True;
  AboutMemo.WordWrap := True;
  AboutMemo.ScrollBars := ssVertical;
  AboutMemo.Lines.Text :=
    'About DAV Converter:' + #13#10 +
    '------------------------' + #13#10 +
    'Version: 1.0' + #13#10 +
    'Author: Mozahid Islam' + #13#10 +
    'This tool was built to help users convert CCTV .dav video files to standard .mp4 format easily.' + #13#10 +
    'Includes ffmpeg backend for fast performance.';
end;
