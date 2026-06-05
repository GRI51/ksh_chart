@echo off
setlocal

pushd %~dp0

set success_run=
set python_ver=3.11
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo 仮想環境の実行に失敗しました。
    goto end
)

@REM PyLint
echo PyLint実行中...
set pylint_report_file=static_analysis_reports\pylint.txt
pylint src/ --rcfile pylintrc --output %pylint_report_file%
type %pylint_report_file%
@REM Flake8
echo Flake8実行中...
set flake8_report_file=static_analysis_reports\flake8.txt
flake8 src/ --config flake8.ini --verbose > %flake8_report_file%
type %flake8_report_file%
@REM mypy
echo mypy実行中...
set mypy_report_file=static_analysis_reports\mypy.txt
mypy src/ --config-file mypy.ini --html-report static_analysis_reports --txt-report static_analysis_reports > %mypy_report_file%
type %mypy_report_file%
@REM pytest実行とカバレッジ取得
python -m pytest tests/ --cov=src --cov-report xml
if %errorlevel% neq 0 (
    echo pytestの実行に失敗しました。
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
