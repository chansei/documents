@echo off
chcp 65001 >nul

setlocal ENABLEDELAYEDEXPANSION

echo.
echo =========================
echo Windows10 ESU登録修正スクリプト
echo =========================

:: --- 管理者チェック ---
openfiles > nul 2>&1
if not %ERRORLEVEL% == 0 (
  echo [-] This command prompt is NOT ELEVATED!
  goto L_end
)

echo.
echo === 0) 事前準備 ===
echo □WindowsのアカウントはMicrosoftアカウントに紐付けされていますか
echo □設定アプリにて「アカウント」-「Windowsバックアップ」で「設定の同期」を有効にしていますか
echo □Windowsは最新の状態に更新されていますか（Windows Updateで「最新の状態です」と表示されていますか）
echo.
echo 上記を確認したら Enter キーを押してください．
pause

echo.
echo === 1) DiagTrack を自動起動に設定し，起動する ===
sc.exe qc DiagTrack >nul 2>&1
if errorlevel 1 (
  echo DiagTrack サービスが見つかりません．
) else (
  sc.exe config DiagTrack start= auto
  sc.exe start DiagTrack
)

echo.
echo === 2) 機能フラグをレジストリに設定（4011992206=2） ===
set "KEY=HKLM\SYSTEM\CurrentControlSet\Policies\Microsoft\FeatureManagement\Overrides"
:: 事前にバックアップ
reg.exe export "%KEY%" "%~dp0Overrides_backup.reg" /y >nul 2>&1
:: 値の投入
reg.exe add "%KEY%" /v 4011992206 /t REG_DWORD /d 2 /f

echo.
echo === 3) 関連ページを起動（手動確認用） ===
:: 同期設定（Microsoft アカウントでの同期を一度有効にする）
start "" ms-settings:sync
:: Windows Update
start "" ms-settings:windowsupdate
:: Edge の[ヘルプとフィードバック]→[Microsoft Edge について]相当
start "" microsoft-edge:edge://settings/help

echo.
echo === 4) 直後の確認（存在すれば表示） ===
reg.exe query "HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows\ConsumerESU" /v ESUEligibility 2>nul

echo.
echo 完了しました．PCを再起動してから状態を確認してください．
pause

:L_end
echo.
echo 管理者として再度実行してください．
pause