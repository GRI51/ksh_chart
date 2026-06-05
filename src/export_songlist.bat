@echo off
setlocal

pushd %~dp0

set success_run=
set package_name=GRI_REMIX2


call ..\.venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo 仮想環境の実行に失敗しました。
    goto end
)

python export_songlist.py %package_name%
if %errorlevel% neq 0 (
    echo export_songlist.pyの実行に失敗しました。
    goto end
)

set success_run=1

:end
popd
if defined success_run (
    exit /b 0
) else (
    exit /b -1
)
