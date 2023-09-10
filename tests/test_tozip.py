import os
import tempfile

import pytest
from pytest_mock.plugin import MockerFixture

import tozip


class TestToZip:
    """単体テスト
    """

    def test_tozip(self, mocker: MockerFixture):
        with tempfile.TemporaryDirectory() as tempfolder:
            # pyファイルを実行
            tozip.export_zip(tempfolder)
            # zipファイルの一覧を取得
            zip_list = os.listdir(tempfolder)
            # 拡張子を除去
            for i, z_name in enumerate(zip_list):
                zip_list[i] = os.path.splitext(z_name)[0]
            # songs
            songs = os.listdir(os.path.join(os.path.dirname(
                __file__), '..', 'src', 'songs'))
            for song in songs:
                s_name = os.path.basename(song)
                assert s_name in zip_list, f'{s_name}がzip化されていません。'
            # packagesフォルダ内のフォルダがzip化されているか確認
            packages = os.listdir(os.path.join(os.path.dirname(
                __file__), '..', 'src', 'packages'))
            for package in packages:
                p_name = os.path.basename(package)
                assert p_name in zip_list, f'{p_name}がzip化されていません。'
