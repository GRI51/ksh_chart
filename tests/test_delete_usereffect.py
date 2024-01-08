import os
import shutil
import tempfile

import pytest

import delete_usereffect


class TestDeleteUsereffect:
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
    def test_delete_usereffect(self, ksh_path):
        with tempfile.TemporaryDirectory() as temp_folder:
            # テスト用ファイルを一時ファイルにコピー
            shutil.copy2(ksh_path, temp_folder)
            # pyファイルを実行
            delete_usereffect.main(ksh_path)
            # 検証
            backup_ksh = os.path.normpath(os.path.join(os.path.dirname(
                __file__), '..', 'src', 'backup', os.path.basename(ksh_path)))
            assert os.path.isfile(backup_ksh), 'バックアップファイルが生成されていません。'
            os.remove(backup_ksh)

    @pytest.mark.parametrize('ksh_path, expect', [
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh',
         'illegal_user_effect_fx.ksh'), 'FXエフェクト構文解析エラー。バージョン変更等により譜面形式が変更されている可能性があります。'),
        (os.path.join(os.path.dirname(__file__), 'testksh', 'illegal_ksh',
         'illegal_user_effect_filter.ksh'), 'Filterエフェクト構文解析エラー。バージョン変更等により譜面形式が変更されている可能性があります。'),
    ])
    def test_delete_usereffect_error_ksh_format(self, ksh_path, expect):
        with tempfile.TemporaryDirectory() as temp_folder:
            # テスト用ファイルを一時ファイルにコピー
            shutil.copy2(ksh_path, temp_folder)
            # 検証
            with pytest.raises(ValueError) as err:
                delete_usereffect.main(ksh_path)
            assert str(err.value) == expect, 'エラーメッセージが期待値と一致しません。'
