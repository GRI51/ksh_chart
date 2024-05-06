import argparse
import os

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from check_module import check_bt_clap_overlap

urllib3.disable_warnings(InsecureRequestWarning)
# 無理押しチェッカーWebサイトのURL
REQUEST_URL = 'https://owatatsu.pasta-soft.com/k2/kshoot/muri_checker/muri_checker.php'
# タイムアウト（単位[sec.]）
REQUEST_TIMEOUT = 20


def main(ksh_path: str) -> bool:
    """1.kshファイルを読み込みます。
    2.kshファイルから特定につながる情報を削除します。
    3.無理押しチェッカーにリクエスト送信します。
    4.結果をコンソール表示します。

    Parameters
    ----------
    ksh_path : str
        kshファイルのパス
    """

    # print('バージョン1.71のkshファイルに対応しています。')
    # print(f'{os.path.basename(ksh_path)} に無理押しが含まれるか判定します。')

    # バリデーション
    # 存在確認
    if not os.path.isfile(ksh_path):
        print(f'ファイルが見つかりませんでした。処理を中止します。{ksh_path}')
        return False
    # 拡張子確認
    if os.path.splitext(ksh_path)[1] != '.ksh':
        print(f'拡張子がkshではありません。処理を中止します。{ksh_path}')
        return False

    # kshファイル読み込み
    with open(ksh_path, mode='r', newline="", encoding="utf_8_sig") as f:
        ksh_text = f.readlines()

    # BTとSE付きFXの重なりをチェック
    is_bt_clap_overlap, pos = check_bt_clap_overlap(ksh_text)
    if is_bt_clap_overlap:
        print('！！！BTとSE付きFXの重なりが含まれています！！！')
        print('　小節数', pos)

    # kshファイルから特定につながる情報を削除
    for i, row in enumerate(ksh_text):
        # イコール（=）を含む場合は、イコールの右辺を削除
        if '=' in row:
            split_row = row.split('=')
            ksh_text[i] = split_row[0] + '=' + '\n'
        # コメント行は削除
        if row.startswith('#'):
            ksh_text[i] = ''

    # POST通信を実行
    request_data = {'score': ''.join(ksh_text)}
    response = requests.post(REQUEST_URL, data=request_data, verify=False, timeout=20)

    # POST通信結果を表示
    if response.status_code != 200:
        print('HTTPステータスが200ではありません。無理押しチェッカーWebサイトとのアクセスに失敗しました。')
        print(f'HTTPステータスコード:{response.status_code}')
        return False
    murioshi_result = response.content.decode()
    murioshi_result = murioshi_result.split("</form><br><br>")[1].split("<br><br><hr>")[0]
    # 無理押しがあった場合にコンソール表示
    if 'error code' in murioshi_result:
        print(ksh_path)
        print(murioshi_result)
        print()
    return True


if __name__ == "__main__":
    # 2. パーサを作る
    parser = argparse.ArgumentParser(description='Delete not used user effects.')
    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('ksh_path', help='ksh file directroy.')
    # 4. 引数を解析
    args = parser.parse_args()

    main(args.ksh_path)
