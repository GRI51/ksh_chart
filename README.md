# ksh_chart
[![.github/workflows/main.yaml](https://github.com/GRI51/ksh_chart/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/GRI51/ksh_chart/actions/workflows/main.yaml)
[![pages-build-deployment](https://github.com/GRI51/ksh_chart/actions/workflows/pages/pages-build-deployment/badge.svg?branch=main)](https://github.com/GRI51/ksh_chart/actions/workflows/pages/pages-build-deployment)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/GRI51/4ebfb53821948ae141d18fac58571b88/raw/pytest-coverage-comment.json)](https://github.com/GRI51/ksh_chart/actions/workflows/main.yaml)

GRIが製作したK-Shoot mania向け譜面を公開するWebページ

## Webページ
[公開しているWebページへのリンク](https://gri51.github.io/ksh_chart/ "https://gri51.github.io/ksh_chart/")

## How To Use
1. 配布したいkshファイルやパッケージを所定のフォルダに格納する
1. GitHubリポジトリにファイルをPUSHする
1. CIが自動的にパッケージ配布用zipと配布用Webページ（htmlファイル）を作成する
1. Webページを共有することで譜面を公開することができます

## リリース手順
1. `src/packages`または`src/songs`にパッケージを格納する。
1. `export_songlist.bat`の`package_name`という変数にエクスポートしたいパッケージ名を指定する。
1. `export_songlist.bat`を実行する。
1. 生成されたhtmlファイルを引用し、`docs`フォルダ内に配布ページ（html）を作成する。
1. ソースコードをパッケージごとpushする。
1. 問題ないことを確認したらdevelopmentブランチをmainブランチにマージする。

## ToDo
- CIに無理押し判定を追加
- カバレッジの改善　`（if __name == '__main__')`の中身もテスト
- Languagesの判定から.kshファイルを除外（できるか不明）
- CIに差分元パッケージダウンロード＋パス指定が正しいかの判定を追加
- CIでzip化したファイルを解凍して`kshootmania.exe`で再生できるかテスト
- 譜面紹介動画の自動生成
