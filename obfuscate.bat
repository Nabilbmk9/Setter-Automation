@echo off
pyarmor gen main.py
pyarmor gen config
pyarmor gen services
pyarmor gen controllers
pyarmor gen hooks
pyarmor gen ui
pyarmor gen utils

xcopy /E /Y ms-playwright dist/