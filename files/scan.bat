@echo off
chcp 65001 > nul

whoami /priv | find "SeDebugPrivilege" > nul
if %errorlevel% neq 0 (
    powershell start-process "%~0" -verb runas
    exit
)

:MAIN

    for /f "usebackq delims=" %%a in (`ver`) do set version=%%a
    if %PROCESSOR_ARCHITECTURE%==AMD64 (set bit=64) else (set bit=32)

    echo 【コマンド開始：%date% %time%】
    echo.

    echo **** デバイス情報(メーカー，型番，製造番号)
    echo.

    wmic csproduct get IdentifyingNumber,Name,Vendor

    echo **** スペック情報(CPU)
    echo.

    wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors

    echo **** スペック情報(メモリ)
    echo.

    powershell -NoProfile -ExecutionPolicy Unrestricted %~dp0\mem.ps1

    echo **** オペレーティングシステム情報(プロダクト名，プロダクトバージョン，アーキテクチャ)
    echo.

    wmic os get caption,version,osarchitecture

    echo いずれかのキーを押すとシステスキャンを開始します...
    pause > nul
    echo.
    
:SCAN

    echo **** システムスキャン(sfc，dism)
    echo.

    sfc /scannow
    dism /online /cleanup-image /restorehealth

    echo.
    pause
