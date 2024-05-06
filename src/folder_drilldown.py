"""引数で指定されたディレクトリをドリルダウンし、
下層のフォルダも含んでkshファイルを探索する。
kshファイルのファイルパスを要素として持つlistを返却する。
"""
import argparse
import os

# 引数のフォルダの中からkshファイルのファイルパスを探索した
# 結果を格納しておくテキストファイルの名称
FILENAME = 'kshpath.txt'


def main(folder_path: str) -> list[str]:
    """フォルダの中からファイル一覧を取得し、
    kshファイルのファイルパスを要素として持つlistを返却する。

    Parameters
    ----------
    folder_path : str
        探索したいディレクトリのファイルパス

    Returns
    -------
    list[str]
        kshファイルのファイルパスを要素として持つlist
    """
    ksh_list = []
    # ディレクトリを走査
    for root, _, files in os.walk(folder_path):
        for file in files:
            # kshファイルのみ抽出
            ext = os.path.splitext(file)[-1]
            if ext == '.ksh':
                ksh_list.append(os.path.join(root, file))
    # このフォルダより下の階層で見つかったkshファイルを返却
    return ksh_list


if __name__ == "__main__":
    # 2. パーサを作る
    parser = argparse.ArgumentParser(description='Delete not used user effects.')
    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('ksh_path', help='ksh file directroy.')
    # 4. 引数を解析
    args = parser.parse_args()

    # kshファイルを探索
    ksh_list = main(args.ksh_path)
    # # 各要素の前後にダブルクォーテーション（"）を追加
    # ksh_list = list(map(lambda x: '"'+x+'"', ksh_list))
    # 各要素の末尾に改行コードを追加
    ksh_list = list(map(lambda x: x+'\n', ksh_list))
    # 結果をファイル出力
    output_path = os.path.join(os.path.dirname(__file__), FILENAME)
    with open(output_path, mode='w', encoding='utf-8') as f:
        f.writelines(ksh_list)
