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
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(song_info_list)


def csv_to_html_with_colspan(input_file: str, output_file: str) -> bool:
    if os.path.splitext(input_file)[1].lower() != '.csv':
        logger.warning(f'入力ファイルの拡張子がcsvではありません。処理を中止します。{input_file}')
        return False
    elif not os.path.isfile(input_file):
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
    with open(input_csv_path, 'r') as file_br:
        url = 'https://mugen-tools.com/tools/table.php'
        data = ''.join(file_br.readlines())
        try:
            res = requests.post(url=url, data={'input': data}, timeout=30)
        except TimeoutError:
            logger.warning('webサイトへのPOST通信に失敗しました。', exc_info=True)
            return False
    # レスポンスの値が200以外だった場合は中止
    if res.status_code != 200:
        logger.warning(f'webサイトへのPOST通信に失敗しました。ステータスコード：{res.status_code} レスポンスの内容：{res.text}')
        return False
    # 必要部分のみ抽出
    soup = BeautifulSoup(res.text, 'html.parser')
    html_text = str(soup.find('textarea', id='outText'))
    # レベル20を赤字太字に変換
    html_text = html_text.replace('<td>20</td>', '<td><b><font color="red">20</font></b></td>')
    # ファイルとして保存
    if output_html_path is None:
        output_html_path = input_csv_path.replace(os.path.splitext(input_csv_path)[1], '.html')
    with open(output_html_path, 'w', encoding='utf-8', newline='') as htmlfile:
        htmlfile.writelines(res.content.decode('utf_8'))
    return True
