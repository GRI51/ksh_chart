@echo off
setlocal

set success_make_env=
set python_ver=3.13

pushd "%~dp0"
cd ..

echo Python%python_ver%仮想環境を構築します。

py -%python_ver% -m pip install -U pip
if %errorlevel% neq 0 (
    echo pipのアップデートに失敗しました。
    goto end
)

py -%python_ver% -m pip install -U setuptools
if %errorlevel% neq 0 (
    echo setuptoolsのアップデートに失敗しました。
    goto end
)
@REM ここから仮想環境内で作業する
py -%python_ver% -m venv .venv
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo 仮想環境の起動に失敗しました。
    goto end
)

python -m pip install -U pip
if %errorlevel% neq 0 (
    echo 仮想環境のpipのアップデートに失敗しました。
    goto end
)

python -m pip install -r installation/development.txt
if %errorlevel% neq 0 (
    echo 開発用Pythonライブラリのインストールに失敗しました。
    goto end
)

python -m pip install -r installation/requirements.txt
if %errorlevel% neq 0 (
    echo Pythonライブラリのインストールに失敗しました。
    goto end
)

set success_make_env=True

:end
popd
if defined success_make_env (
    echo 環境構築に成功しました！
    python -V
    pause
    exit /b 0
) else (
    echo 環境構築に失敗しました。
    pause
    exit /b -1
)
