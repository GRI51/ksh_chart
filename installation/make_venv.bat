@echo off
setlocal

set success_make_env=
set python_ver=3.11
@REM 仮想環境をプロジェクト直下に作る
set PIPENV_VENV_IN_PROJECT=1

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

py -%python_ver% -m pip install pipenv
if %errorlevel% neq 0 (
    echo pipenvのアップデートに失敗しました。
    goto end
)

py -%python_ver% -m pipenv install -d -r installation/development.txt
if %errorlevel% neq 0 (
    echo 開発用Pythonライブラリのインストールに失敗しました。
    goto end
)

py -%python_ver% -m pipenv install -r installation/requirements.txt
if %errorlevel% neq 0 (
    echo Pythonライブラリのインストールに失敗しました。
    goto end
)

set success_make_env=True

:end
popd
if defined success_make_env (
    echo 環境構築に成功しました！
    py -%python_ver% -m pipenv run python -V
    pause
    exit /b 0
) else (
    echo 環境構築に失敗しました。
    pause
    exit /b -1
)
