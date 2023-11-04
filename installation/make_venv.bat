@echo off
setlocal

set success_make_env=
set python_ver=3.11

pushd "%~dp0"
cd ..

echo Python%python_ver%���z�����\�z���܂��B

py -%python_ver% -m venv .venv
if %errorlevel% neq 0 (
    echo Python%python_ver%��������܂���ł����B
    goto end
)

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ���z���̎��s�Ɏ��s���܂����B
    goto end
)

py -m pip install -U pip
if %errorlevel% neq 0 (
    echo pip�̃A�b�v�f�[�g�Ɏ��s���܂����B
    goto end
)

py -m pip install -U setuptools
if %errorlevel% neq 0 (
    echo setuptools�̃A�b�v�f�[�g�Ɏ��s���܂����B
    goto end
)

py -m pip install pipenv
if %errorlevel% neq 0 (
    echo pipenv�̃A�b�v�f�[�g�Ɏ��s���܂����B
    goto end
)

pipenv install -d -r installation/development.txt
if %errorlevel% neq 0 (
    echo �J���pPython���C�u�����̃C���X�g�[���Ɏ��s���܂����B
    goto end
)

pipenv install -r installation/requirements.txt
if %errorlevel% neq 0 (
    echo Python���C�u�����̃C���X�g�[���Ɏ��s���܂����B
    goto end
)

set success_make_env=True

:end
popd
if defined success_make_env (
    echo ���\�z�ɐ������܂����I
    python -V
    pause
    exit /b 0
) else (
    echo ���\�z�Ɏ��s���܂����B
    pause
    exit /b -1
)
