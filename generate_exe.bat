@echo off
call ./obfuscate.bat

cd build\windows

rd /s /q "build"
rd /s /q "dist"
pyinstaller main_obfuscate.spec