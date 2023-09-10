import os

import pytest

import libs


class TestLibs:
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
    def test_get_file_encoding(self, ksh_path):
        assert os.path.isfile(
            ksh_path), f'入力ファイルが見つかりません。{os.path.normpath(os.path.abspath(ksh_path))}'
        encoding = libs.get_file_encoding(ksh_path)
        # 戻り値を検証
        assert encoding == 'UTF-8-SIG', f'取得した文字コードが不正です。入力ファイル：{os.path.normpath(os.path.abspath(ksh_path))}、文字コード{encoding}'
