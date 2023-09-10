import sys
import os
import pathlib
import tempfile

import pytest

import export_songlist


class TestExportSonglist:
    """単体テスト
    """
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
    def test_export_songlist(self, ksh_path: str | pathlib.Path, song_info: dict):
        assert os.path.isfile(
            ksh_path), f'入力ファイルが見つかりません。{os.path.normpath(os.path.abspath(ksh_path))}'
        s_info = export_songlist.export_package_songlist([ksh_path])
        s_info = s_info[0]
        # 戻り値を検証
        assert s_info['title'] == song_info['title'], 'タイトルが一致していません'
        assert s_info['artist'] == song_info['artist'], 'アーティスト名が一致していません'
        assert s_info['effect'] == song_info['effect'], '譜面製作者名が一致していません'
        assert s_info.get('LT') == song_info.get('LT'), 'LTの難易度（1～20）が一致していません'
        assert s_info.get('CH') == song_info.get('CH'), 'CHの難易度（1～20）が一致していません'
        assert s_info.get('EX') == song_info.get('EX'), 'EXの難易度（1～20）が一致していません'
        assert s_info.get('IN') == song_info.get('IN'), 'INの難易度（1～20）が一致していません'
        assert s_info['source'] == song_info['source'], '出典が一致していません'

    def test_to_csv(self):
        # listを準備
        song_info_list = [{'title': 'Astral spirits[PIN]', 'artist': 'K-forest', 'effect': 'GRI', 'EX': '17', 'source': 'SFES2019'},
                          {'title': 'Clck Up[respectBCH]', 'artist': 'Sho Fish',
                              'effect': 'GRI S-Style', 'IN': '18', 'source': 'SF2016 No.31-60'},
                          {'title': 'Dirigeant Decision[respectF]', 'artist': 'siqlo',
                              'effect': 'GRI', 'IN': '17', 'source': 'SF2016 No.31-60'},
                          {'title': 'Ethereal Ray[modern]', 'artist': 'yoho',
                              'effect': 'GRI', 'IN': '19', 'source': 'SF2016 No.31-60'},
                          {'title': 'Meishin-Midnight[respect7&F]', 'artist': 'Ask.A',
                              'effect': 'GRI', 'IN': '16', 'source': 'SFES2022'},
                          {'title': 'Neverending Nightmare[wow]', 'artist': 'Dragon_Klub',
                              'effect': 'GRI', 'IN': '18', 'source': 'SFES2020'},
                          {'title': 'Out of Range[respectSG]', 'artist': 'xima',
                              'effect': 'GRI', 'EX': '17', 'source': 'SFES2020'},
                          {'title': 'Out of Range[respect99]', 'artist': 'xima',
                              'effect': 'GRI', 'IN': '19', 'source': 'SFES2020'},
                          {'title': 'O.V.E.R.[SSS]', 'artist': 'xima',
                              'effect': 'GRI SSS-Style', 'IN': '17', 'source': 'SFES2022'},
                          {'title': 'Retribution[OH]', 'artist': 'brz1128+すいマグ',
                              'effect': 'GRI', 'IN': '18', 'source': 'Pastel breeze vol.3'},
                          {'title': 'Kaiser die Traumerei[respectN]', 'artist': 'K2 overture',
                              'effect': 'GRI', 'IN': '19', 'source': 'Eupholic Selections vol.1'},
                          {'title': 'Regression to Zero[respectCHT]', 'artist': 'seatrus', 'effect': 'GRI',
                              'EX': '17', 'IN': '19', 'source': 'Eupholic Selections vol.2'},
                          {'title': '%UnDeciphered-CryptoGraph in the Edifice%[modern]', 'artist': 'seatrus',
                              'effect': 'GRI', 'IN': '18', 'source': 'Eupholic Selections vol.1'},
                          {'title': 'Variant Cross[modern]', 'artist': 'M-UE', 'effect': 'GRI', 'IN': '17', 'source': 'Eupholic Selections vol.1'}]
        # 一時フォルダにcsv出力
        with tempfile.TemporaryDirectory() as tmpdirname:
            csv_path = os.path.join(
                tmpdirname, sys._getframe().f_code.co_name + '.csv')
            export_songlist.to_csv(song_info_list, csv_path)
            # 検証
            # 生成したcsvファイルが存在するか
            assert os.path.isfile(csv_path), 'csvファイルが見つかりませんでした。'
            # csvファイルの中身が正しいか
            with open(csv_path, mode='r', encoding='utf_8') as csv_file:
                csv_text = csv_file.readlines()
            assert csv_text[0].strip(
            ) == 'title,artist,effect,LT,CH,EX,IN,source', 'ヘッダーに記載されているテキストが異常です。'
            for i, song_info in enumerate(song_info_list):
                expect_row = ''.join(song_info.values())
                assert csv_text[i + 1].strip().replace(',',
                                                       '') == expect_row, 'ヘッダーに記載されているテキストが異常です。'

    def test_to_html(self):
        # csvファイルを準備
        song_info_list = [{'title': 'Astral spirits[PIN]', 'artist': 'K-forest', 'effect': 'GRI', 'EX': '17', 'source': 'SFES2019'},
                          {'title': 'Clck Up[respectBCH]', 'artist': 'Sho Fish',
                              'effect': 'GRI S-Style', 'IN': '18', 'source': 'SF2016 No.31-60'},
                          {'title': 'Dirigeant Decision[respectF]', 'artist': 'siqlo',
                              'effect': 'GRI', 'IN': '17', 'source': 'SF2016 No.31-60'},
                          {'title': 'Ethereal Ray[modern]', 'artist': 'yoho',
                              'effect': 'GRI', 'IN': '19', 'source': 'SF2016 No.31-60'},
                          {'title': 'Meishin-Midnight[respect7&F]', 'artist': 'Ask.A',
                              'effect': 'GRI', 'IN': '16', 'source': 'SFES2022'},
                          {'title': 'Neverending Nightmare[wow]', 'artist': 'Dragon_Klub',
                              'effect': 'GRI', 'IN': '18', 'source': 'SFES2020'},
                          {'title': 'Out of Range[respectSG]', 'artist': 'xima',
                              'effect': 'GRI', 'EX': '17', 'source': 'SFES2020'},
                          {'title': 'Out of Range[respect99]', 'artist': 'xima',
                              'effect': 'GRI', 'IN': '19', 'source': 'SFES2020'},
                          {'title': 'O.V.E.R.[SSS]', 'artist': 'xima',
                              'effect': 'GRI SSS-Style', 'IN': '17', 'source': 'SFES2022'},
                          {'title': 'Retribution[OH]', 'artist': 'brz1128+すいマグ',
                              'effect': 'GRI', 'IN': '18', 'source': 'Pastel breeze vol.3'},
                          {'title': 'Kaiser die Traumerei[respectN]', 'artist': 'K2 overture',
                              'effect': 'GRI', 'IN': '19', 'source': 'Eupholic Selections vol.1'},
                          {'title': 'Regression to Zero[respectCHT]', 'artist': 'seatrus', 'effect': 'GRI',
                              'EX': '17', 'IN': '19', 'source': 'Eupholic Selections vol.2'},
                          {'title': '%UnDeciphered-CryptoGraph in the Edifice%[modern]', 'artist': 'seatrus',
                              'effect': 'GRI', 'IN': '18', 'source': 'Eupholic Selections vol.1'},
                          {'title': 'Variant Cross[modern]', 'artist': 'M-UE', 'effect': 'GRI', 'IN': '17', 'source': 'Eupholic Selections vol.1'}]
        # 一時フォルダにcsv出力
        with tempfile.TemporaryDirectory() as tmpdirname:
            csv_path = os.path.join(
                tmpdirname, sys._getframe().f_code.co_name + '.csv')
            export_songlist.to_csv(song_info_list, csv_path)
            html_path = os.path.join(
                tmpdirname, sys._getframe().f_code.co_name + '.html')
            assert export_songlist.to_html(
                csv_path, html_path), 'メソッドの実行に失敗しました。'
            # htmlファイルを生成できたか確認
            assert os.path.isfile(html_path), 'htmlファイルが見つかりませんでした。'
            # htmlの中身を検証
            with open(html_path, mode='r', encoding='utf_8') as html_file:
                html_text = html_file.readlines()
            assert html_text[4].strip(
            ) == '<title>CSVをHTML Tableに変換【みんなの知識 ちょっと便利帳】</title>', 'htmlファイルの中身が異常です。'
            assert html_text[15].strip(
            ) == "<table class='t'>", 'htmlファイルの中身が異常です。'

    def test_to_html2(self):
        """引数1つ　拡張子.csvを.htmlに変換
        """
        # csvファイルを準備
        song_info_list = [{'title': 'Astral spirits[PIN]', 'artist': 'K-forest', 'effect': 'GRI', 'EX': '17', 'source': 'SFES2019'},
                          {'title': 'Clck Up[respectBCH]', 'artist': 'Sho Fish',
                              'effect': 'GRI S-Style', 'IN': '18', 'source': 'SF2016 No.31-60'},
                          {'title': 'Dirigeant Decision[respectF]', 'artist': 'siqlo',
                              'effect': 'GRI', 'IN': '17', 'source': 'SF2016 No.31-60'},
                          {'title': 'Ethereal Ray[modern]', 'artist': 'yoho',
                              'effect': 'GRI', 'IN': '19', 'source': 'SF2016 No.31-60'},
                          {'title': 'Meishin-Midnight[respect7&F]', 'artist': 'Ask.A',
                              'effect': 'GRI', 'IN': '16', 'source': 'SFES2022'},
                          {'title': 'Neverending Nightmare[wow]', 'artist': 'Dragon_Klub',
                              'effect': 'GRI', 'IN': '18', 'source': 'SFES2020'},
                          {'title': 'Out of Range[respectSG]', 'artist': 'xima',
                              'effect': 'GRI', 'EX': '17', 'source': 'SFES2020'},
                          {'title': 'Out of Range[respect99]', 'artist': 'xima',
                              'effect': 'GRI', 'IN': '19', 'source': 'SFES2020'},
                          {'title': 'O.V.E.R.[SSS]', 'artist': 'xima',
                              'effect': 'GRI SSS-Style', 'IN': '17', 'source': 'SFES2022'},
                          {'title': 'Retribution[OH]', 'artist': 'brz1128+すいマグ',
                              'effect': 'GRI', 'IN': '18', 'source': 'Pastel breeze vol.3'},
                          {'title': 'Kaiser die Traumerei[respectN]', 'artist': 'K2 overture',
                              'effect': 'GRI', 'IN': '19', 'source': 'Eupholic Selections vol.1'},
                          {'title': 'Regression to Zero[respectCHT]', 'artist': 'seatrus', 'effect': 'GRI',
                              'EX': '17', 'IN': '19', 'source': 'Eupholic Selections vol.2'},
                          {'title': '%UnDeciphered-CryptoGraph in the Edifice%[modern]', 'artist': 'seatrus',
                              'effect': 'GRI', 'IN': '18', 'source': 'Eupholic Selections vol.1'},
                          {'title': 'Variant Cross[modern]', 'artist': 'M-UE', 'effect': 'GRI', 'IN': '17', 'source': 'Eupholic Selections vol.1'}]
        # 一時フォルダにcsv出力
        with tempfile.TemporaryDirectory() as tmpdirname:
            csv_path = os.path.join(
                tmpdirname, sys._getframe().f_code.co_name + '.csv')
            export_songlist.to_csv(song_info_list, csv_path)
            html_path = os.path.join(
                tmpdirname, sys._getframe().f_code.co_name + '.html')
            assert export_songlist.to_html(
                csv_path), 'メソッドの実行に失敗しました。'
            # htmlファイルを生成できたか確認
            assert os.path.isfile(html_path), 'htmlファイルが見つかりませんでした。'
            # htmlの中身を検証
            # htmlの中身を検証
            with open(html_path, mode='r', encoding='utf_8') as html_file:
                html_text = html_file.readlines()
            assert html_text[4].strip(
            ) == '<title>CSVをHTML Tableに変換【みんなの知識 ちょっと便利帳】</title>', 'htmlファイルの中身が異常です。'
            assert html_text[15].strip(
            ) == "<table class='t'>", 'htmlファイルの中身が異常です。'
