import logging
import os
import tempfile

import pytest
from pytest_mock.plugin import MockerFixture

import tozip


class TestToZip:
    """単体テスト
    """

    def test_export_zip(self):
        """export_zipを引数ありで実行します
        """
        with tempfile.TemporaryDirectory() as tempfolder:
            # pyファイルを実行
            tozip.export_zip(tempfolder)
            # zipファイルの一覧を取得
            zip_list = os.listdir(tempfolder)
            # 拡張子を除去
            for i, z_name in enumerate(zip_list):
                zip_list[i] = os.path.splitext(z_name)[0]
            # songs
            songs = os.listdir(os.path.join(os.path.dirname(__file__), '..', 'src', 'songs'))
            for song in songs:
                s_name = os.path.basename(song)
                assert s_name in zip_list, f'{s_name}がzip化されていません。'
            # packagesフォルダ内のフォルダがzip化されているか確認
            packages = os.listdir(os.path.join(os.path.dirname(__file__), '..', 'src', 'packages'))
            for package in packages:
                p_name = os.path.basename(package)
                assert p_name in zip_list, f'{p_name}がzip化されていません。'

    def test_export_zip_with_no_args(self, mocker: MockerFixture):
        """export_zipを引数無しで実行します

        Parameters
        ----------
        mocker : MockerFixture
            os.path.joinのモック
        """
        with tempfile.TemporaryDirectory() as tempfolder:
            mocker.patch('os.path.join', return_value=tempfolder)
            # pyファイルを実行
            tozip.export_zip()
            # zipファイルの一覧を取得
            zip_list = os.listdir(tempfolder)
            # 拡張子を除去
            for i, z_name in enumerate(zip_list):
                zip_list[i] = os.path.splitext(z_name)[0]
            # songs
            songs = os.listdir(os.path.join(os.path.dirname(__file__), '..', 'src', 'songs'))
            for song in songs:
                s_name = os.path.basename(song)
                assert s_name in zip_list, f'{s_name}がzip化されていません。'
            # packagesフォルダ内のフォルダがzip化されているか確認
            packages = os.listdir(os.path.join(os.path.dirname(__file__), '..', 'src', 'packages'))
            for package in packages:
                p_name = os.path.basename(package)
                assert p_name in zip_list, f'{p_name}がzip化されていません。'

    def test_export_zip_errorcase(self, mocker: MockerFixture, caplog: pytest.LogCaptureFixture):
        """ファイルが見つからない場合の準正常系動作確認。

        Parameters
        ----------
        mocker : MockerFixture
            shutil.make_archiveのモック　意図的に例外を出す
        """
        caplog.set_level(logging.INFO)
        mocker.patch("shutil.make_archive", side_effect=FileNotFoundError())
        with tempfile.TemporaryDirectory() as tempfolder:
            # pyファイルを実行
            tozip.export_zip(tempfolder)
        # 例外発生時のメッセージを検証
        for log_message in caplog.records:
            assert log_message.message == 'フォルダが見つかりません。zipファイルの生成に失敗しました。', '例外メッセージが期待値と一致しません。'
