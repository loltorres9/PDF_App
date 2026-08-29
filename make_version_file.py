"""Schreibt version_info.txt für PyInstaller — die Eigenschaften der Exe.

Ohne diese Datei zeigt Windows im Rechtsklick → Eigenschaften nichts an und
SmartScreen hat noch weniger, woran es das Programm erkennen kann. Die Version
kommt aus ``pdfmerge_core.__version__``, damit sie nur an einer Stelle steht.

    python make_version_file.py
"""

from __future__ import annotations

from pdfmerge_core import __version__

COMPANY = "PDF-Merger"
PRODUCT = "PDF-Merger"
DESCRIPTION = "PDF-Dateien zusammenfügen"

TEMPLATE = """VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({major}, {minor}, {patch}, 0),
    prodvers=({major}, {minor}, {patch}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0),
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '040704b0',
          [
            StringStruct('CompanyName', '{company}'),
            StringStruct('FileDescription', '{description}'),
            StringStruct('FileVersion', '{version}'),
            StringStruct('InternalName', 'PDF-Merger'),
            StringStruct('OriginalFilename', 'PDF-Merger.exe'),
            StringStruct('ProductName', '{product}'),
            StringStruct('ProductVersion', '{version}'),
          ],
        )
      ]
    ),
    # 0x0407 = Deutsch, 0x04b0 = Unicode. Muss zur StringTable oben passen.
    VarFileInfo([VarStruct('Translation', [0x0407, 1200])]),
  ],
)
"""


def main() -> None:
    major, minor, patch = (int(part) for part in __version__.split("."))
    with open("version_info.txt", "w", encoding="utf-8") as handle:
        handle.write(
            TEMPLATE.format(
                major=major,
                minor=minor,
                patch=patch,
                version=__version__,
                company=COMPANY,
                product=PRODUCT,
                description=DESCRIPTION,
            )
        )
    print(f"version_info.txt geschrieben (Version {__version__})")


if __name__ == "__main__":
    main()
