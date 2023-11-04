"""kshファイルが格納されたフォルダをzipに変換します。
"""
import glob
import os
import shutil

import libs.python_logger

logger = libs.python_logger.set_logger(__name__)


def make_zip(zip_name: str, target_folder: str) -> bool:
    # 改行コードをCRLFに変換
    glob_path = os.path.join(target_folder, '**', '*.ksh')
    ksh_list = glob.glob(glob_path, recursive=True)
    for ksh_path in ksh_list:
        with open(ksh_path, 'r', encoding='utf-8-sig') as oldfile:
            txt = oldfile.read()
        with open(ksh_path, 'w', encoding='utf-8-sig', newline='\r\n') as newfile:
            newfile.write(txt)
    # zip化
    folder_name = os.path.basename(target_folder)
    dir_name = os.path.dirname(target_folder)
    try:
        output_path = shutil.make_archive(zip_name, format='zip', root_dir=dir_name, base_dir=folder_name)
        logger.info(f'zipファイルの生成に成功しました。出力先：{output_path}')
        return True
    except FileNotFoundError:
        logger.error('フォルダが見つかりません。zipファイルの生成に失敗しました。', exc_info=True)
        return False


def export_zip(output_dir: str | None = None) -> None:
    # 出力先フォルダ
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets')
    # 個別の個人配布譜面をzip化
    song_folders = os.listdir(os.path.join(os.path.dirname(__file__), 'songs'))
    for folder_name in song_folders:
        root_dir = os.path.join(os.path.dirname(__file__), 'songs', folder_name)
        zip_name = os.path.join(output_dir, folder_name)
        make_zip(zip_name, root_dir)
    # パッケージをzip化
    package_folders = os.listdir(os.path.join(os.path.dirname(__file__), 'packages'))
    for folder_name in package_folders:
        zip_name = os.path.join(output_dir, folder_name)
        root_dir = os.path.join(os.path.dirname(__file__), 'packages', folder_name)
        make_zip(zip_name, root_dir)
