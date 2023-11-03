@echo off
setlocal

pushd %~dp0

@REM PyLint
echo PyLint実行中...
pylint src/ --rcfile pylintrc --output static_analysis_reports/pylint.txt
@REM Flake8
echo Flake8実行中...
flake8 src/ --config flake8.ini --verbose > static_analysis_reports/flake8.txt
@REM bandit
echo bandit実行中...
bandit -r src/ --configfile bandit.yaml -f html --output static_analysis_reports/bandit.html
@REM mypy
echo mypy実行中...
mypy src/ --config-file mypy.ini --html-report static_analysis_reports --txt-report static_analysis_reports > static_analysis_reports/mypy.txt

popd
