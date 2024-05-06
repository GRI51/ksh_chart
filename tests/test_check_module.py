import os

import pytest

import check_module


class TestCheckModule:
    """テストクラス
    """
    @pytest.mark.parametrize('ksh_path, expect_bool, expect_pos', [(
        os.path.join(os.path.dirname(
            __file__), 'testksh', 'BEYOND_THE_LiMiT_560_GRI.ksh'), False, None),
        (os.path.join(os.path.dirname(
            __file__), 'testksh', 'Raving_Vibes_GRI.ksh'), False, None),
        (os.path.join(os.path.dirname(
            __file__), 'testksh', 'pianodokusoukyoku_akaikutsu_GRI.ksh'), False, None),
        (os.path.join(os.path.dirname(
            __file__), 'testksh', 'gypsy_GRI.ksh'), True, [53]),
        (os.path.join(os.path.dirname(
            __file__), 'testksh', 'BURST_V_GRI.ksh'), True, [76, 78]),
    ])
    def test_check_bt_clap_overlap(self, ksh_path: str, expect_bool: bool, expect_pos: list[int] | None) -> None:
        """BTとSE付きFXの重なりのテスト
        FTとSE無しFXは対象外

        Parameters
        ----------
        ksh_path : str
            テスト用kshファイル
        expect : bool
            期待値 BTとSE付きFXの重なりが含まれていれば`True`
        """
        # 存在確認
        assert os.path.isfile(ksh_path), f'ファイルが見つかりませんでした。処理を中止します。{ksh_path}'
        # 拡張子確認
        assert os.path.splitext(ksh_path)[1] == '.ksh', f'拡張子がkshではありません。処理を中止します。{ksh_path}'
        # kshファイル読み込み
        with open(ksh_path, mode='r', newline="", encoding="utf_8_sig") as f:
            ksh_text = f.readlines()
            # テスト対象関数実行
            ret, pos = check_module.check_bt_clap_overlap(ksh_text)
        # 期待値と比較
        assert ret == expect_bool, '重なり有無の判定結果が期待値と一致しません。'
        assert pos == expect_pos, '重なりがある位置が期待値と一致しません。'
