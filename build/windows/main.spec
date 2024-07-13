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
    ['../../dist/main.py'],
    pathex=['../../'],
    binaries=binaries,
    datas=[
        ('../../dist/config/', 'config'),
        ('../../dist/config/user_config.json', 'config'),
        ('../../dist/config/app_config.json', 'config'),
        ('../../dist/ms-playwright', './_internal/ms-playwright'),
        ('../../dist/pyarmor_runtime_000000/', 'pyarmor_runtime'),
        ('../../dist/ui/', 'ui'),
        ('../../dist/utils/', 'utils'),
        ('../../dist/services/', 'services'),
        ('../../dist/controllers/', 'controllers'),
        ('../../dist/hooks/', 'hooks')
        # Ajoutez d'autres fichiers et dossiers nécessaires ici
    ] + datas,
    hiddenimports=hiddenimports + [
        'playwright.sync_api',
        'sqlite3',
        'dotenv',
        'PySide6',
        'PySide6.QtWidgets',
        'cryptography',
        'cryptography.fernet',
        'requests'
    ],
    hookspath=['hooks'],
    runtime_hooks=[],
    excludes=[],
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
    console=False,
    version="version.txt"
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
