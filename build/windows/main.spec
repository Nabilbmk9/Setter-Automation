# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

# Collecter toutes les dépendances nécessaires pour sqlite3
datas, binaries, hiddenimports = collect_all('sqlite3')

# Ajouter manuellement les fichiers DLL nécessaires
python_dlls = os.path.join(sys.base_prefix, 'DLLs')
binaries += [
    (os.path.join(python_dlls, 'sqlite3.dll'), '.'),
    (os.path.join(python_dlls, '_sqlite3.pyd'), '.')
]

block_cipher = None

a = Analysis(
    ['../../main.py'],
    pathex=['../../'],
    binaries=binaries,
    datas=[
        ('config/user_config.json', '.'),
        ('config/app_config.json', '.'),
        ('../../ms-playwright', './_internal/ms-playwright')
    ] + datas,
    hiddenimports=hiddenimports + [
        'playwright.sync_api',
        'sqlite3',
        'dotenv'
    ],
    hookspath=['hooks'],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='linkedin_automation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='linkedin_automation'
)
