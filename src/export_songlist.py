"""パッケージに収録する楽曲の情報をまとめてcsv形式で出力します。
"""
import csv
import os
import re
import requests
from bs4 import BeautifulSoup

import libs.python_logger
import songinfo

logger = libs.python_logger.set_logger(__name__)


def export_package_songlist(ksh_paths: list[str]) -> list[songinfo.SongInfo]:
    """`songinfo.get_package_song_info()`を用いてkshファイル群の情報を取得する

    Parameters
    ----------
    ksh_paths : list[str]
        kshファイルのパスを要素として持つ`list`

    Returns
    -------
    list[dict]
        入力されたkshファイルに対応する情報が格納された`list`
    """
    song_list: list[songinfo.SongInfo] = []
    for song_path in ksh_paths:
        song_info = songinfo.get_package_song_info(song_path)
        song_list.append(song_info)
    return song_list


def to_csv(song_info_list: list[songinfo.SongInfo], output_csv_path: str) -> None:
    """楽曲情報（アーティスト名や難易度など）をcsvに変換してファイル出力する。

    Parameters
    ----------
    song_info_list : list[songinfo.SongInfo]
        楽曲情報 songinfo.get_package_song_info()で取得する
    output_csv_path : str
        出力先のcsvファイルパス
    """
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['title', 'artist', 'effect', 'LT', 'CH', 'EX', 'IN', 'source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(song_info_list)


def csv_to_html_with_colspan(input_file: str, output_file: str) -> bool:
    """csvファイルの内容をhtmlの表形式に変換して保存する。

    Parameters
    ----------
    input_file : str
        入力するcsvファイルのパス
    output_file : str
        出力するhtmlファイルのパス

    Returns
    -------
    bool
        変換と保存に成功したら`True`を、失敗したら`False`を返す。
    """
    if os.path.splitext(input_file)[1].lower() != '.csv':
        logger.warning(f'入力ファイルの拡張子がcsvではありません。処理を中止します。{input_file}')
        return False
    if not os.path.isfile(input_file):
        logger.warning(f'入力ファイルが見つかりませんでした。処理を中止します。{input_file}')
        return False
    if output_file is None:
        output_file = input_file.replace(os.path.splitext(input_file)[1], '.html')
    elif os.path.splitext(output_file)[1].lower() != '.html':
        logger.warning(f'出力ファイルの拡張子がhtmlではありません。処理を中止します。{output_file}')
        return False

    with open(input_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        html_text: list[str] = []

        html_text.append("<!DOCTYPE html>\n")
        html_text.append("<html><head><title>CSV to HTML Table</title></head><body>\n")
        html_text.append("<table border='1'>\n")

        for row_index, row in enumerate(reader):
            html_text.append("<tr>\n")
            empty_count = 0
            for cell in row:
                if cell == "":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        tag = "th" if row_index == 0 else "td"
                        html_text.append(f"<{tag} colspan='{empty_count}'></{tag}>\n")
                        empty_count = 0
                    tag = "th" if row_index == 0 else "td"
                    html_text.append(f"<{tag}>{cell}</{tag}>\n")
            if empty_count > 0:
                tag = "th" if row_index == 0 else "td"
                html_text.append(f"<{tag} colspan='{empty_count}'></{tag}>\n")
            html_text.append("</tr>\n")

        html_text.append("</table>\n")
        html_text.append("</body></html>\n")
    # レベル20を赤字太字に変換
    html_text = [line.replace('<td>20</td>', '<td><b><font color="red">20</font></b></td>') for line in html_text]
    html_text = [re.sub(r'<td>20\.([0-9]{1})</td>', r'<td><b><font color="red">20.\1</font></b></td>', line)
                 for line in html_text]
    # ファイルとして保存
    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.writelines(html_text)
    return True


if __name__ == '__main__':
    import glob
    import sys

    # ここでどのパッケージ情報を取得するか指定
    glob_path = os.path.join(os.path.dirname(__file__), 'packages', sys.argv[1], '*', '*.ksh')
    print(glob_path)

    export_ksh_paths = glob.glob(glob_path)
    s_info_list = export_package_songlist(export_ksh_paths)

    # to csv
    csv_path = os.path.join(os.path.dirname(__file__), 'songlist.csv')
    to_csv(s_info_list, csv_path)

    # to html
    # csv->html変換サイトへPOST通信
    html_path = os.path.join(os.path.dirname(__file__), 'songlist.html')
    csv_to_html_with_colspan(csv_path, html_path)
