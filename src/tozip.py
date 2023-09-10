"""kshファイルが格納されたフォルダをzipに変換します。
"""
import shutil
import os


def export_zip(output_dir=None):
    # 出力先フォルダ
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(
            __file__), '..', 'docs', 'assets')
    # 個別の個人配布譜面をzip化
    folders = os.listdir(os.path.join(os.path.dirname(__file__), 'songs'))
    for folder_name in folders:
        zip_name = os.path.join(output_dir, folder_name)
        root_dir = os.path.join(os.path.dirname(
            __file__), 'songs', folder_name)
        try:
            output_path = shutil.make_archive(
                zip_name, format='zip', root_dir=root_dir)
            print(f'zipファイルの生成に成功しました。出力先：{output_path}')
        except Exception as err:
            print(err)

    # パッケージをzip化
    folders = os.listdir(os.path.join(os.path.dirname(__file__), 'packages'))
    for folder_name in folders:
        zip_name = os.path.join(output_dir, folder_name)
        root_dir = os.path.join(os.path.dirname(
            __file__), 'packages', folder_name)
        try:
            output_path = shutil.make_archive(
                zip_name, format='zip', root_dir=root_dir)
            print(f'zipファイルの生成に成功しました。出力先：{output_path}')
        except Exception as err:
            print(err)


if __name__ == '__main__':
    export_zip()
