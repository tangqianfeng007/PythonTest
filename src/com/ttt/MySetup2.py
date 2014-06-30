from cx_Freeze import setup, Executable

includes=["smtplib", "pyHook"]

exe = Executable(
script="svhosts.py",
base="Win32Gui",
targetName = "D:/pyexe/svhosts.exe"
)

setup(
name = "hello",
version = "this is test hosts",
description = "description",
options = {"build_exe": {"includes":includes}},
executables = [exe]
)