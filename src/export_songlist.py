"""パッケージに収録する楽曲の情報をまとめてcsv形式で出力します。
"""
import csv
import os
from typing import Final

import requests

import libs.python_logger
import songinfo

CSV_TO_HTML_WEBSITE_URL: Final[str] = 'https://www.benricho.org/moji_conv/csv-to-table/csv-to-table.php'
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
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(song_info_list)


def to_html(input_csv_path: str, output_html_path: str | None = None) -> bool:
    """csvファイルを表形式のhtmlに変換する。

    Parameters
    ----------
    input_csv_path : str
        htmlの表に変換したいcsvのファイルパス
    output_html_path : str | None, optional
        出力するhtmlファイル名（ファイルパス）, by default None

    Returns
    -------
    bool
        htmlファイルへの変換と保存に成功したら`True`を、失敗したら`False`を返す。
    """
    with open(input_csv_path, 'rb') as file_br:
        files = {'file': file_br}
        try:
            res = requests.post(url=CSV_TO_HTML_WEBSITE_URL, files=files, timeout=30)
        except TimeoutError:
            logger.warning('webサイトへのPOST通信に失敗しました。', exc_info=True)
            return False
    # バイトから復元
    html_text = res.content.decode('utf_8')
    # レベル20を赤字太字に変換
    html_text = html_text.replace(
        '<td>20</td>', '<td><b><font color="red">20</font></b></td>')
    # ファイルとして保存
    if output_html_path is None:
        output_html_path = input_csv_path.replace(
            os.path.splitext(input_csv_path)[1], '.html')
    with open(output_html_path, 'w', encoding='utf-8', newline='') as htmlfile:
        htmlfile.writelines(res.content.decode('utf_8'))
    return True
