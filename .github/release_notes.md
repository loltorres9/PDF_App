**PDF-Merger {TAG}** — PDF-Dateien auswählen, Reihenfolge festlegen, zu einer Datei zusammenfügen.

| Datei | Wofür |
|---|---|
| **`PDF-Merger-Setup.exe`** | **Empfohlen.** Installer: Startmenü-Eintrag, auf Wunsch Desktop-Symbol und ein Eintrag unter *Senden an*. Installiert nur für den angemeldeten Benutzer, ohne Administratorrechte. |
| `PDF-Merger.exe` | Das Programm als einzelne Datei, ganz ohne Installation. Speichern und starten. |

Python wird auf dem Zielrechner nicht gebraucht.

## Windows warnt beim Herunterladen und beim Start

Das ist erwartbar: die Dateien sind **nicht signiert** — ein Code-Signing-Zertifikat kostet mehrere hundert Euro im Jahr — und SmartScreen kennt jede neue Datei zunächst nicht. Es sagt nichts darüber aus, was in der Datei ist.

1. **Beim Herunterladen** („wird nicht häufig heruntergeladen"): im Download-Menü des Browsers *Beibehalten* → *Trotzdem beibehalten*.
2. **Beim ersten Start** („Der Computer wurde durch Windows geschützt"): *Weitere Informationen* → *Trotzdem ausführen*.
3. Alternativ vorher entsperren: Rechtsklick auf die Datei → *Eigenschaften* → unten *Zulassen* ankreuzen → *OK*. In PowerShell: `Unblock-File .\PDF-Merger-Setup.exe`.

Wer lieber nachrechnet, statt zu vertrauen: die Prüfsummen unten stammen aus genau dem Build, der diese Dateien erzeugt hat ([Workflow](https://github.com/loltorres9/PDF_App/blob/main/.github/workflows/windows-build.yml), Quellcode im Repository).

```powershell
Get-FileHash .\PDF-Merger-Setup.exe -Algorithm SHA256
```

| Datei | SHA-256 |
|---|---|
{HASHES}

Dieselben Werte liegen dem Release als `SHA256SUMS.txt` bei.
