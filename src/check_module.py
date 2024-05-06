"""無理押し・準無理押し・好ましくない配置の
有無を判定するための関数群
"""


def check_bt_clap_overlap(ksh_data: list[str]) -> tuple[bool, list[int] | None]:
    """ BTとSE付きFXの重なりをチェック
    fx-l_se=clap_punchy;55
    fx-r_se=clap_punchy;55
    0000|22|--

    Parameters
    ----------
    ksh_data : list[str]
        kshファイルの中身をreadlines()で読み込んだ値

    Returns
    -------
    bool
        BTとSE付きFXの重なりの有無。
        重なりがあれば`True`を返す。
        重なりがなければ`False`を返す。
    """
    # 重なりがあることを示すための変数。重なりがあればTrue。
    check_result = False
    # 重なりがあった場所の小節数
    syosetsu_no = 0
    position: list[int] | None = []
    # SEの指示文があるときにTrueになる変数
    # SEの指示文（fx-r_se=clap_punchy;55）と
    # 譜面データ（0000|22|--）が異なる行にあるので、フラグで管理する。
    fxchip_l_se_flag = False
    fxchip_r_se_flag = False
    for row in ksh_data:
        # 文字列の前後の空白と改行コードを削除
        row = row.strip()
        # 小節数をカウントアップ
        if row == '--':
            syosetsu_no += 1
        # =でセパレート
        row_split = row.split('=')
        if len(row_split) >= 2:
            # SEの指示文があるかチェック
            if 'fx-l_se' in row_split[0]:
                fxchip_l_se_flag = True
                continue
            if 'fx-r_se' in row_split[0]:
                fxchip_r_se_flag = True
                continue
        elif len(row_split) == 1:
            # 行の値が10文字（0000|22|--）であるか確認
            if len(row) == 10:
                # FXチップが配置されているかチェック
                is_fx_l_chip = row[5] == '2'
                is_fx_r_chip = row[6] == '2'
                # BTチップが配置されているかチェックj
                is_bt_l_chip = row[0] == '1' or row[1] == '1'
                is_bt_r_chip = row[2] == '1' or row[3] == '1'
                # 重なりがあるかチェック
                if fxchip_l_se_flag and is_fx_l_chip and is_bt_l_chip:
                    check_result = True
                    position.append(syosetsu_no)
                elif fxchip_r_se_flag and is_fx_r_chip and is_bt_r_chip:
                    check_result = True
                    position.append(syosetsu_no)
                # Fフラグリセット
                fxchip_l_se_flag = False
                fxchip_r_se_flag = False
        else:
            raise ValueError('ファイルの構文解析中にエラーが発生しました。')
    # 判定後の後処理
    if not check_result:
        # 重なりが存在しなければ小節位置に関する情報はNoneにする
        position = None
    else:
        # リスト内の重複を削除
        position = list(set(position))
    return check_result, position
