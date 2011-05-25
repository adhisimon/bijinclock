#!/usr/bin/env python
from cx_Freeze import setup, Executable

exe = Executable(
    script = "bijinclock.py",
    base = "Win32GUI"
)
setup(
    name = "bijinclock",
    version = "0.9.9",
    description = "Bijin Clock",
    executables = [exe],
    options = {
        "build_exe": {
            "include_files": [
                "gtkrc",
                ("COPYING", "COPYING.txt"),
                ("gtk+_2.22.1-1_win32/share/themes", "share/themes"),
                ("gtk+_2.22.1-1_win32/lib", "lib"),
                ("gtk+_2.22.1-1_win32/etc", "etc"),
            ],
            "icon": "bijinclock.ico"
        }
    }
)
