@echo off
setlocal

pushd %~dp0

set success_run=

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo 仮想環境の実行に失敗しました。
    goto end
)

@REM PyLint
echo PyLint実行中...
pylint src/ --rcfile pylintrc --output static_analysis_reports/pylint.txt
@REM Flake8
echo Flake8実行中...
flake8 src/ --config flake8.ini --verbose > static_analysis_reports/flake8.txt
@REM mypy
echo mypy実行中...
mypy src/ --config-file mypy.ini --html-report static_analysis_reports --txt-report static_analysis_reports > static_analysis_reports/mypy.txt
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
