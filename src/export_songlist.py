"""パッケージに収録する楽曲の情報をまとめてcsv形式で出力します。
"""
import pathlib
import songinfo
import csv
import os

import requests


def export_package_songlist(ksh_paths: list[str | pathlib.Path]) -> list[dict]:
    """songinfo.get_package_song_info()を用いてkshファイル群の情報を取得する

    Parameters
    ----------
    ksh_paths : list[str  |  pathlib.Path]
        kshファイルのパスを要素として持つlist

    Returns
    -------
    list[dict]
        入力されたkshファイルに対応する情報が格納されたlist
    """
    song_list: list[dict] = []
    for song_path in ksh_paths:
        song_info = songinfo.get_package_song_info(song_path)
        for s_info in song_list:
            if s_info['title'] == song_info['title']:
                s_info.update(song_info)
                break
        else:
            song_list.append(song_info)
    return song_list


def to_csv(song_info_list: list, output_csv_path: str) -> None:
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['title', 'artist',
                      'effect', 'LT', 'CH', 'EX', 'IN', 'source']
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
        htmlファイルへの変換と保存に成功したらTrueを、失敗したらFalseを返す。
    """
    files = {'file': open(input_csv_path, 'rb')}
    CSV_TO_HTML_WEBSITE_URL = 'https://www.benricho.org/moji_conv/csv-to-table/csv-to-table.php'
    try:
        res = requests.post(url=CSV_TO_HTML_WEBSITE_URL,
                            files=files, timeout=30)
    except TimeoutError as err:
        print("webサイトへのPOST通信に失敗しました。")
        print(err)
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


if __name__ == '__main__':
    import glob

    glob_path = os.path.join(os.path.dirname(
        __file__), 'packages', 'GRI_REMIX', '*', '*.ksh')
    export_ksh_paths = glob.glob(glob_path)
    s_info_list = export_package_songlist(export_ksh_paths)
    assert s_info_list[0]['title'] == 'Astral spirits[PIN]', 'タイトルが一致していません'
    assert s_info_list[0]['artist'] == 'K-forest', 'アーティスト名が一致していません'
    assert s_info_list[0]['effect'] == 'GRI', '譜面製作者名が一致していません'
    assert s_info_list[0]['EX'] == '17', 'extendedの難易度（1～20）が一致していません'
    assert s_info_list[0]['source'] == 'SFES2019', '出典が一致していません'

    # to csv
    csv_path = os.path.join(
        os.path.dirname(__file__), 'songlist.csv')
    to_csv(s_info_list, csv_path)

    # to html
    # csv->html変換サイトへPOST通信
    to_html(csv_path)
