# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['app\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('venv/lib/site-packages/customtkinter', 'customtkinter/'),
    ('app/resources/icons/switch_button.png', 'resources/icons'),
    ('app/resources/icons/google_translate_logo.ico', 'resources/icons')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Google Translate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app/resources/icons/google_translate_logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Google Translate',
)
