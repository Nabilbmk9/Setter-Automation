@echo off
rd /s /q "dist"

pyarmor gen main.py
pyarmor gen config
pyarmor gen services
pyarmor gen controllers
pyarmor gen hooks
pyarmor gen ui
pyarmor gen utils

xcopy ms-playwright dist\ms-playwright /E /I /Y
xcopy config\default_config\user_config.json dist\config\ /Y
xcopy config\app_config.json dist\config\ /Y
xcopy ui\resources dist\ui\resources /E /I /Y
