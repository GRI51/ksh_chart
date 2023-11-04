import argparse
import os
import shutil
from typing import Final

import libs.python_logger

KSH_FILE_FORMAT_VER: Final[float] = 1.71
logger = libs.python_logger.set_logger(__name__)


def main(ksh_path: str) -> None:
    """kshファイルから一度も使われていないユーザー定義エフェクトを削除します。

    Parameters
    ----------
    ksh_path : str
        kshファイルパス

    Raises
    ------
    TypeError
        引数が文字列でないとき
    FileNotFoundError
        引数で指定したファイルが見つからないとき
    ValueError
        引数で指定したファイルkshファイルでないとき
    """
    logger.info(f'バージョン{KSH_FILE_FORMAT_VER}のkshファイルに対応しています。')
    # バリデーション
    # 引数の型チェック
    if not isinstance(ksh_path, str):
        raise TypeError(f'引数ksh_pathはstr型である必要があります。入力された変数の型：{type(ksh_path)}')
    # ファイルの存在チェック
    if not os.path.isfile(ksh_path):
        abs_path = os.path.normpath(os.path.abspath(ksh_path))
        raise FileNotFoundError(f'譜面ファイルが見つかりませんでした。{abs_path}')
    # kshファイルのみを受け付ける
    if os.path.splitext(ksh_path)[1] != '.ksh':
        abs_path = os.path.normpath(os.path.abspath(ksh_path))
        raise ValueError(f'.kshファイルのみ変換が可能です。{abs_path}')
    logger.info(f'{os.path.basename(ksh_path)} から1度も使われていないユーザー定義エフェクトを削除します。')

    # ファイルから使われているエフェクト名を解析し、利用されてないエフェクトを削除したリストnew_kshを作成
    new_ksh = []
    used_fx_effect_name = []
    used_filter_effect_name = []
    with open(ksh_path, 'r', newline="", encoding="utf_8_sig") as ksh_file:
        datalist = ksh_file.readlines()
        for row in datalist:
            if 'fx-r_se=' in row or 'fx-l_se=' in row:
                pass
            # ユーザー定義エフェクト（FX）が使われたか判定
            elif '#define_fx' in row:
                used_fx = set(used_fx_effect_name)
                fx_name = row.split(' ')[1]
                if fx_name not in used_fx:
                    continue    # 一度も使われていないエフェクトはスキップ
            # ユーザー定義エフェクト（レーザー）
            elif '#define_filter' in row:
                used_filter = set(used_filter_effect_name)
                filter_name = row.split(' ')[1]
                if filter_name not in used_filter:
                    continue    # 一度も使われていないエフェクトはスキップ
            # 譜面中で使われたFXエフェクトを取得
            elif 'fx-' in row:
                if row[:5] not in ('fx-l=', 'fx-r='):
                    raise ValueError('FXエフェクト構文解析エラー。バージョン変更等により譜面形式が変更されている可能性があります。')
                fx_effectname = row[5:].split(';')[0].rstrip('\r\n')
                used_fx_effect_name.append(fx_effectname)
            # 譜面中で使われたレーザーエフェクトを取得
            elif 'filtertype' in row:
                filter_effectname = row[11:].rstrip('\r\n')
                if ';' in filter_effectname:
                    raise ValueError('Filterエフェクト構文解析エラー。バージョン変更等により譜面形式が変更されている可能性があります。')
                used_filter_effect_name.append(filter_effectname)
            elif 'filter:' in row:
                filter_effectname = row.split(':')[1]
                used_filter_effect_name.append(filter_effectname)
            new_ksh.append(row)
    # バックアップを作成
    backup_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'backup', os.path.basename(ksh_path))
    if not os.path.isdir(os.path.dirname(backup_path)):
        os.makedirs(os.path.dirname(backup_path))
    backup_path = checkfile(backup_path)
    if os.path.exists(backup_path):
        backup_path = backup_path.replace('.ksh', '_1.ksh')
    shutil.move(ksh_path, backup_path)  # 古いファイルを保存
    logger.info(f'バックアップファイルを保存しました。 {backup_path}')

    # 新たなファイルを保存
    with open(ksh_path, 'w', newline="", encoding="utf_8_sig") as ksh_file:
        ksh_file.writelines(new_ksh)

    logger.info(f'{os.path.basename(ksh_path)} から1度も使われていないユーザー定義エフェクトを削除しました。')


def checkfile(path: str, max_no: int = 9) -> str:
    """既にファイルが存在するか確認し、存在する場合は末尾に通し番号を付けて置き換える。

    Parameters
    ----------
    path : str
        存在するか確認するパス

    Returns
    -------
    str
        新しいパス
    """
    # 型チェック
    if not isinstance(max_no, int) or max_no <= 0:
        raise ValueError(f'max_noは自然数を指定して下さい。max_no={max_no}')
    # 存在しない最も若い通し番号を判別し、パスにして返す
    newpath = path
    if os.path.exists(path):
        for no in range(max_no):
            newpath = path.replace('.ksh', f'_{no}.ksh')
            if not os.path.exists(newpath):
                break
    return newpath


if __name__ == "__main__":
    # 2. パーサを作る
    parser = argparse.ArgumentParser(
        description='Delete not used user effects.')
    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('ksh_path', help='ksh file directroy.')
    # 4. 引数を解析
    args = parser.parse_args()

    main(args.ksh_path)
