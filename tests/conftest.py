import logging
import os
import shutil
import sys
import tempfile
from logging.handlers import TimedRotatingFileHandler

import pytest

# srcフォルダのpyhonファイルをimportできるようにする
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# テスト用ログファイル保存先の有無チェック
LOG_FILE = os.path.normpath(os.path.join(
    os.path.dirname(__file__), 'logs', 'test_event_log.log'))
LOG_DIR = os.path.dirname(LOG_FILE)
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)
# ファイルハンドラの設定
file_handler = TimedRotatingFileHandler(LOG_FILE, when='D', interval=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s@Test log@[%(levelname)s]- %(name)s - %(funcName)s : %(message)s")
)
# ルートロガーの設定
logging.basicConfig(level=logging.NOTSET, handlers=[file_handler])


# @pytest.fixture(scope='session', autouse=True)
# def setup_inifile():
#     # 前処理
#     ini_path = os.path.join(os.path.dirname(__file__),
#                             '..', 'src', 'config.ini')
#     tmpdir = tempfile.TemporaryDirectory()
#     shutil.copy2(ini_path, tmpdir.name)
#     yield
#     # 後処理
#     shutil.copy2(os.path.join(
#         tmpdir.name, os.path.basename(ini_path)), ini_path)
#     tmpdir.cleanup()


# # 関数の差し替え
# def dummy_func(*args, **kwargs) -> None:
#     pass


# def mock_timer(prompt='', time_out=60.0, t=[0]):
#     """この関数を所定の回数呼び出したら、'q'を返す。

#     Parameters
#     ----------
#     prompt : str, optional
#         _description_, by default ''
#     time_out : float, optional
#         _description_, by default 60.0
#     t : list, optional
#         この関数を呼び出した回数を保持するための変数, by default [0]

#     Returns
#     -------
#     _type_
#         所定回数より多くこの関数を呼び出したら'q',そうでなければNoneを返す
#     """
#     LIMIT_TIME = 100
#     t[0] = t[0] + 1
#     if t[0] > LIMIT_TIME:
#         ret = 'q'
#     else:
#         ret = None
#     return ret
