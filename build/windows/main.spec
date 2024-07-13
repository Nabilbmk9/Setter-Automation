# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

# Collecter toutes les dépendances nécessaires pour sqlite3
datas, binaries, hiddenimports = collect_all('sqlite3')

a = Analysis(
    ['../../main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas + [
        ('../../config/user_config.json', 'config'),
        ('../../config/app_config.json', 'config'),
        ('../../ms-playwright', './_internal/ms-playwright')
    ],
    hiddenimports=hiddenimports + [
        'playwright.sync_api',
        'sqlite3',
        'dotenv'
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='linkedin_automation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version="version.txt"
)
