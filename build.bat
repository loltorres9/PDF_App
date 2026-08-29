@echo off
REM Baut PDF-Merger.exe - eine einzelne Datei, die ohne Python laeuft -
REM und, falls Inno Setup installiert ist, zusaetzlich den Installer.
REM
REM Fertige Dateien gibt es auch ohne diesen Schritt unter
REM https://github.com/loltorres9/PDF_App/releases
REM
REM Voraussetzung: Python 3.9+ ist installiert und in PATH.
setlocal
cd /d "%~dp0"

echo [1/4] Abhaengigkeiten installieren...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt pyinstaller || goto :fehler

echo [2/4] Versionsinfo schreiben...
python make_version_file.py || goto :fehler

echo [3/4] Exe bauen...
python -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name "PDF-Merger" ^
  --icon app.ico ^
  --add-data "app.ico;." ^
  --version-file version_info.txt ^
  --collect-submodules pypdf ^
  pdfmerge.py || goto :fehler

echo [4/4] Installer bauen (nur mit Inno Setup)...
set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if exist "%ISCC%" (
  "%ISCC%" installer.iss || goto :fehler
  echo Fertig: "%~dp0dist\PDF-Merger.exe" und "%~dp0installer_out\PDF-Merger-Setup.exe"
) else (
  echo Inno Setup nicht gefunden - Installer uebersprungen.
  echo Zu holen unter https://jrsoftware.org/isdl.php, dann dieses Skript erneut starten.
  echo Fertig: "%~dp0dist\PDF-Merger.exe"
)

start "" "%~dp0dist"
goto :ende

:fehler
echo.
echo Build fehlgeschlagen - siehe Meldungen oben.
exit /b 1

:ende
endlocal
