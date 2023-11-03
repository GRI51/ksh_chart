@echo off
setlocal

pushd %~dp0

@REM PyLint
echo PyLint���s��...
pylint src/ --rcfile pylintrc --output static_analysis_reports/pylint.txt
@REM Flake8
echo Flake8���s��...
flake8 src/ --config flake8.ini --verbose > static_analysis_reports/flake8.txt
@REM bandit
echo bandit���s��...
bandit -r src/ --configfile bandit.yaml -f html --output static_analysis_reports/bandit.html
@REM mypy
echo mypy���s��...
mypy src/ --config-file mypy.ini --html-report static_analysis_reports --txt-report static_analysis_reports > static_analysis_reports/mypy.txt

popd
