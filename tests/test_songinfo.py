import os

import pytest

import songinfo


class TestSongInfo:
    """単体テスト
    """
    @pytest.mark.parametrize('ksh_path', [
        os.path.join(os.path.dirname(
            __file__), 'testksh', 'AstralSpirits[PIN]', 'AstralSpirits_ex[PIN].ksh'),
        os.path.join(os.path.dirname(
            __file__), 'testksh', 'DirigeantDecision[respectN]', 'IN[respectN].ksh'),
        os.path.join(os.path.dirname(
            __file__), 'testksh', 'Rv-27 [modern]', 'Rv-27 [modern].ksh'),
        os.path.join(os.path.dirname(
            __file__), 'testksh', 'イザヨイレイバース[PAN]', 'izayoiravers[PAN].ksh'),
    ])
    def test_search_ksh_element(self, ksh_path):
        assert os.path.isfile(
            ksh_path), f'入力ファイルが見つかりません。{os.path.normpath(os.path.abspath(ksh_path))}'
        with open(ksh_path, encoding='utf_8_sig') as kshfile:
            ksh_texts = kshfile.readlines()
        difficulty = songinfo._search_ksh_element(ksh_texts, 'difficulty')
        # 戻り値を検証
        assert difficulty in ['light', 'challenge', 'extended', 'infinite'], f'取得した難易度名が不正です。{difficulty}'

    @pytest.mark.parametrize('ksh_texts, element, expect', [('ksh_text', 'difficulty', "引数target_ksh_listはlist型である必要があります。入力された変数の型：<class 'str'>"),
                                                            (['', '', ''], ['difficulty'], "引数element_wordはstr型である必要があります。入力された変数の型：<class 'list'>"),])
    def test_search_ksh_element_error_case(self, ksh_texts, element, expect):
        with pytest.raises(TypeError) as e:
            songinfo._search_ksh_element(ksh_texts, element)
        # 戻り値を検証
        assert e.value.args[0] == expect, '例外メッセージが期待値と一致しません。'

    @pytest.mark.parametrize('ksh_path, song_info', [
        (os.path.join(os.path.dirname(
            __file__), 'testksh', 'AstralSpirits[PIN]', 'AstralSpirits_ex[PIN].ksh'),
            {'title': 'Astral spirits[PIN]', 'artist': 'K-forest', 'effect': 'GRI', 'EX': '17', 'source': 'SFES2019'}),
        (os.path.join(os.path.dirname(
            __file__), 'testksh', 'DirigeantDecision[respectN]', 'IN[respectN].ksh'),
            {'title': 'Dirigeant Decision[respectF]', 'artist': 'siqlo', 'effect': 'GRI', 'IN': '17', 'source': 'SF2016 No.31-60'}),
        (os.path.join(os.path.dirname(
            __file__), 'testksh', 'Rv-27 [modern]', 'Rv-27 [modern].ksh'),
            {'title': '%UnDeciphered-CryptoGraph in the Edifice%[modern]', 'artist': 'seatrus', 'effect': 'GRI', 'IN': '18', 'source': 'Eupholic Selections vol.1'}),
        (os.path.join(os.path.dirname(
            __file__), 'testksh', 'イザヨイレイバース[PAN]', 'izayoiravers[PAN].ksh'),
            {'title': 'イザヨイレイバース[PAN]', 'artist': 'brz1128', 'effect': 'GRI', 'IN': '17', 'source': 'Pastel breeze vol.3'}),
    ])
    def test_songinfo(self, ksh_path: str, song_info: dict):
        assert os.path.isfile(ksh_path), f'入力ファイルが見つかりません。{os.path.normpath(os.path.abspath(ksh_path))}'
        s_info = songinfo.get_package_song_info(ksh_path)
        # 戻り値を検証
        assert s_info['title'] == song_info['title'], 'タイトルが一致していません'
        assert s_info['artist'] == song_info['artist'], 'アーティスト名が一致していません'
        assert s_info['effect'] == song_info['effect'], '譜面製作者名が一致していません'
        assert s_info.get('LT') == song_info.get('LT'), 'LTの難易度（1～20）が一致していません'
        assert s_info.get('CH') == song_info.get('CH'), 'CHの難易度（1～20）が一致していません'
        assert s_info.get('EX') == song_info.get('EX'), 'EXの難易度（1～20）が一致していません'
        assert s_info.get('IN') == song_info.get('IN'), 'INの難易度（1～20）が一致していません'
        assert s_info['source'] == song_info['source'], '出典が一致していません'

    def test_songinfo_filenotfound(self):
        # FileNotFoundErrorを検知
        dummy_file_name = 'no_file.txt'
        with pytest.raises(FileNotFoundError) as err:
            songinfo.get_package_song_info(dummy_file_name)
        # エラーメッセージを検証
        dummy_file_name = os.path.normpath(os.path.abspath(dummy_file_name))
        assert str(err.value) == f'譜面ファイルが見つかりませんでした。{dummy_file_name}', 'エラーメッセージが期待値と一致しません。'

    @pytest.mark.parametrize('ksh_path, expect', [
        (False, "引数ksh_pathはstr型である必要があります。入力された変数の型：<class 'bool'>"),
    ])
    def test_get_package_song_info_type_error(self, ksh_path, expect):
        with pytest.raises(TypeError) as err:
            songinfo.get_package_song_info(ksh_path)
        # エラーメッセージを検証
        assert str(err.value) == expect, 'エラーメッセージが期待値と一致しません。'

    @pytest.mark.parametrize('ksh_path, expect', [
        (os.path.join(os.path.dirname(__file__), 'noexistpath'),
         f'譜面ファイルが見つかりませんでした。{os.path.join(os.path.dirname(__file__), "noexistpath")}'),
    ])
    def test_get_package_song_info_filenotfound_error(self, ksh_path, expect):
        with pytest.raises(FileNotFoundError) as err:
            songinfo.get_package_song_info(ksh_path)
        # エラーメッセージを検証
        assert str(err.value) == expect, 'エラーメッセージが期待値と一致しません。'

    @pytest.mark.parametrize('ksh_path, expect', [
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh', 'lost_song_info.ksh'), '曲名を判別できませんでした。'),
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh', 'lost_artist_info.ksh'), '作曲者を判別できませんでした。'),
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh', 'lost_charteditor_info.ksh'), '譜面製作者を判別できませんでした。'),
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh', 'lost_difficulty_info.ksh'), '難易度（LT～IN）を判別できませんでした。'),
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh',
         'illegal_difficulty_info.ksh'), '難易度を判別できませんでした。LT,CH,EX,IN以外の文字列が指定されています。'),
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh', 'lost_level_info.ksh'), '難易度（1～20）を判別できませんでした。'),
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh', 'lost_source_info.ksh'), '音源ファイルを判別できませんでした。'),
    ])
    def test_get_package_song_info_value_error(self, ksh_path, expect):
        with pytest.raises(ValueError) as err:
            songinfo.get_package_song_info(ksh_path)
        # エラーメッセージを検証
        assert str(err.value) == expect, 'エラーメッセージが期待値と一致しません。'
