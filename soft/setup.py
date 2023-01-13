import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="dodac",
    version="0.1.2",
    description="Do dac va thong ke so lieu",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
)