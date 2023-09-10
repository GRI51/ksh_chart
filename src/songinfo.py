"""kshファイルを指定して楽曲情報を取得します。
kshファイルの文字コードは「UTF-8 with BOM」です。
"""
import pathlib
import os.path

import libs

REPLACE_LIST = [('light', 'LT'), ('challenge', 'CH'),
                ('extended', 'EX'), ('infinite', 'IN')]


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
        raise TypeError(
            f'引数target_ksh_listはlist型である必要があります。入力された変数の型：{type(target_ksh_list)}')
    if not isinstance(element_word, str):
        raise TypeError(
            f'引数element_wordはstr型である必要があります。入力された変数の型：{type(element_word)}')
    # element_wordの要素が含まれるか1行ずつ検索
    for row_text in target_ksh_list:
        if len(element_word) > len(row_text):
            # 検索したい要素の文字数 > 被検索文字数　なら絶対に違うので次の行へ
            continue
        if element_word == row_text[:len(element_word)]:
            # element_wordの要素が見つかったら、=より右側の要素をreturnする
            ret_text = row_text[len(element_word) + 1:]
            return ret_text.strip()
    # 見つからなかった場合
    return None


def get_package_song_info(ksh_path: str | pathlib.Path) -> dict:
    """引数に指定されたkshファイルの楽曲情報を取得します。
    楽曲情報は「曲名」「アーティスト名」「譜面製作者名」「難易度(4段階)」
    「難易度（1～20）」「出典」が含まれます。
    「出典」は差分元が収録されているパッケージの名称です。

    Parameters
    ----------
    ksh_path : str | pathlib.Path
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
    if not isinstance(ksh_path, (str, pathlib.Path)):
        raise TypeError(
            f'引数ksh_pathはstr型かpathlib.Path型である必要があります。入力された変数の型：{type(ksh_path)}')
    # ファイルの存在チェック
    if not os.path.isfile(ksh_path):
        abs_path = os.path.normpath(os.path.abspath(ksh_path))
        raise FileNotFoundError(f'譜面ファイルが見つかりませんでした。{abs_path}')
    # kshファイルの情報を取得
    encoding = libs.get_file_encoding(ksh_path)
    with open(ksh_path, encoding=encoding) as kshfile:
        ksh_texts = kshfile.readlines()
    song_info = {}
    song_info['title'] = _search_ksh_element(ksh_texts, 'title')
    song_info['artist'] = _search_ksh_element(ksh_texts, 'artist')
    song_info['effect'] = _search_ksh_element(ksh_texts, 'effect')
    difficulty = _search_ksh_element(ksh_texts, 'difficulty')
    for old, new in REPLACE_LIST:
        difficulty = difficulty.replace(old, new)
    song_info[difficulty] = _search_ksh_element(ksh_texts, 'level')
    ogg_path = _search_ksh_element(ksh_texts, 'm')
    try:
        song_info['source'] = ogg_path.split('\\')[2]
    except IndexError:
        # 区切り文字が\ではなく/であった場合
        song_info['source'] = ogg_path.split('/')[2]
    return song_info


if __name__ == '__main__':
    test_ksh_path = os.path.join(os.path.dirname(
        __file__), 'songs', 'GRI_REMIX', 'AstralSpirits[PIN]', 'AstralSpirits_ex[PIN].ksh')
    info = get_package_song_info(test_ksh_path)
    assert info['title'] == 'Astral spirits[PIN]', 'タイトルが一致していません'
    assert info['artist'] == 'K-forest', 'アーティスト名が一致していません'
    assert info['effect'] == 'GRI', '譜面製作者名が一致していません'
    assert info['EX'] == '17', 'EXの難易度（1～20）が一致していません'
    assert info['source'] == 'SFES2019', '出典が一致していません'
