@echo off
setlocal

pushd %~dp0

set success_run=

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ���z���̎��s�Ɏ��s���܂����B
    goto end
)

@REM PyLint
echo PyLint���s��...
pylint src/ --rcfile pylintrc --output static_analysis_reports/pylint.txt
@REM Flake8
echo Flake8���s��...
flake8 src/ --config flake8.ini --verbose > static_analysis_reports/flake8.txt
@REM mypy
echo mypy���s��...
mypy src/ --config-file mypy.ini --html-report static_analysis_reports --txt-report static_analysis_reports > static_analysis_reports/mypy.txt
@REM pytest���s�ƃJ�o���b�W�擾
python -m pytest tests/ --cov=src --cov-report xml
if %errorlevel% neq 0 (
    echo pytest�̎��s�Ɏ��s���܂����B
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
