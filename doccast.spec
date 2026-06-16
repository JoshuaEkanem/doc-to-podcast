# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
   datas=[
    ('templates', 'templates'),
    ('static', 'static'),
    ('voices', 'voices'),
    (r'C:\Users\HP\doc-to-podcast\venv\Lib\site-packages\kokoro_onnx', 'kokoro_onnx'),
    (r'C:\Users\HP\doc-to-podcast\venv\Lib\site-packages\language_tags', 'language_tags'),
    (r'C:\Users\HP\doc-to-podcast\venv\Lib\site-packages\espeakng_loader', 'espeakng_loader'),
],
    hiddenimports=[
    'piper',
    'piper.voice',
    'ollama',
    'flask',
    'fitz',
    'docx',
    'wave',
    'requests',
    'numpy',
    'soundfile',
    'kokoro_onnx',
    'language_tags',
    'language_tags.tags',
    'engineio.async_drivers.threading',
],
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
    name='DocCast',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DocCast',
)