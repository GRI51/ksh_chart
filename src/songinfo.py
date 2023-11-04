"""kshファイルを指定して楽曲情報を取得します。
kshファイルの文字コードは「UTF-8 with BOM」です。
"""
import os.path
from typing import TypedDict

from typing_extensions import NotRequired

from libs.file_manager import get_file_encoding

REPLACE_LIST = [('light', 'LT'), ('challenge', 'CH'),
                ('extended', 'EX'), ('infinite', 'IN')]


class SongInfo(TypedDict):
    title: str
    artist: str
    effect: str
    source: str
    LT: NotRequired[str]
    CH: NotRequired[str]
    EX: NotRequired[str]
    IN: NotRequired[str]


def _search_ksh_element(target_ksh_list: list[str], element_word: str) -> str | None:
    """kshファイルをf.readlines()でlist型に変換した変数から、element_wordの要素を抽出します。
    見つからなかった場合、Noneを返します。

    Parameters
    ----------
    target_ksh_list : list[str]
        kshファイルをf.readlines()でlist型に変換した変数
    element_word : str
        検索したい要素名 kshファイルの=(イコール)の左側にある英語文字列を指定します。

    Returns
    -------
    str
        検索した要素の=の右側にある文字列を返します。
        str.strip()メソッドを適用してからreturnするため、前後の空白文字等は削除されます。
        見つからなかった場合、Noneを返します。

    Raises
    ------
    TypeError
        第1引数target_ksh_listの型がlistでない場合
    TypeError
        第2引数telement_wordの型がstrでない場合
    """
    # 引数の型チェック
    if not isinstance(target_ksh_list, list):
        raise TypeError(f'引数target_ksh_listはlist型である必要があります。入力された変数の型：{type(target_ksh_list)}')
    if not isinstance(element_word, str):
        raise TypeError(f'引数element_wordはstr型である必要があります。入力された変数の型：{type(element_word)}')
    # element_wordの要素が含まれるか1行ずつ検索
    for row_text in target_ksh_list:
        if row_text.startswith(element_word + '='):
            # element_wordと完全一致する行が見つかったら、=より左側の文字列を削除して、右側の要素をreturnする
            ret_text = row_text.replace(element_word + '=', '', 1)
            return ret_text.strip()
    # 見つからなかった場合
    return None


def get_package_song_info(ksh_path: str) -> SongInfo:
    """引数に指定されたkshファイルの楽曲情報を取得します。
    楽曲情報は「曲名」「アーティスト名」「譜面製作者名」「難易度(4段階)」
    「難易度（1～20）」「出典」が含まれます。
    「出典」は差分元が収録されているパッケージの名称です。

    Parameters
    ----------
    ksh_path : str
        楽曲情報を取得したいkshファイルのパスを指定します。

    Returns
    -------
    dict
        「曲名」「アーティスト名」「譜面製作者名」「難易度(4段階)」
        「難易度（1～20）」「出典」を返します。辞書型であり、それぞれ
        以下のようにkeyと対応しています。
        曲名：title
        アーティスト名：artist
        譜面製作者名：effect
        難易度(4段階)：difficulty
        難易度（1～20）：level
        出典：source


    Raises
    ------
    TypeError
        引数がファイルパスでない場合
    FileNotFoundError
        指定されたファイルが見つからなかった場合
    """
    # 引数の型チェック
    if not isinstance(ksh_path, str):
        raise TypeError(f'引数ksh_pathはstr型である必要があります。入力された変数の型：{type(ksh_path)}')
    # ファイルの存在チェック
    if not os.path.isfile(ksh_path):
        abs_path = os.path.normpath(os.path.abspath(ksh_path))
        raise FileNotFoundError(f'譜面ファイルが見つかりませんでした。{abs_path}')
    # kshファイルの情報を取得
    encoding = get_file_encoding(ksh_path)
    with open(ksh_path, encoding=encoding) as kshfile:
        ksh_texts = kshfile.readlines()
    title = _search_ksh_element(ksh_texts, 'title')
    if title is None:
        raise ValueError('曲名を判別できませんでした。')
    artist = _search_ksh_element(ksh_texts, 'artist')
    if artist is None:
        raise ValueError('作曲者を判別できませんでした。')
    effect = _search_ksh_element(ksh_texts, 'effect')
    if effect is None:
        raise ValueError('譜面製作者を判別できませんでした。')
    difficulty = _search_ksh_element(ksh_texts, 'difficulty')
    if difficulty is None:
        raise ValueError('難易度（LT～IN）を判別できませんでした。')
    for old, new in REPLACE_LIST:
        difficulty = difficulty.replace(old, new)
    if difficulty not in ['LT', 'CH', 'EX', 'IN']:
        raise ValueError('難易度を判別できませんでした。LT,CH,EX,IN以外の文字列が指定されています。')
    level = _search_ksh_element(ksh_texts, 'level')
    if level is None:
        raise ValueError('難易度（1～20）を判別できませんでした。')
    ogg_path = _search_ksh_element(ksh_texts, 'm')
    if ogg_path is None:
        raise ValueError('音源ファイルを判別できませんでした。')
    try:
        ogg_path = ogg_path.split('\\')[2]
    except IndexError:
        # 区切り文字が\ではなく/であった場合
        ogg_path = ogg_path.split('/')[2]

    song_info: SongInfo = {'title': title, 'artist': artist, 'effect': effect, 'source': ogg_path}
    song_info[difficulty] = level  # type: ignore
    return song_info
