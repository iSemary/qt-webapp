import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

include_files = ['assets']
options = {"build_exe": {"include_files": include_files}}

executables = [Executable("main.py", base=base, icon='Icon.ico', shortcut_name='Qt Webapp')]

setup(
    name="Qt Webapp",
    version="1.0",
    description="Qt Webapp description",
    options=options,
    executables=executables,
)
