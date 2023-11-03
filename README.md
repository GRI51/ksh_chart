# ksh_chart
[![.github/workflows/main.yaml](https://github.com/GRI51/ksh_chart/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/GRI51/ksh_chart/actions/workflows/main.yaml)
[![pages-build-deployment](https://github.com/GRI51/ksh_chart/actions/workflows/pages/pages-build-deployment/badge.svg?branch=main)](https://github.com/GRI51/ksh_chart/actions/workflows/pages/pages-build-deployment)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/GRI51/4ebfb53821948ae141d18fac58571b88/raw/pytest-coverage-comment.json)](https://github.com/GRI51/ksh_chart/actions/workflows/main.yaml)

GRIが製作したK-Shoot mania向け譜面を公開するWebページ

配布したいkshファイルやパッケージを所定のフォルダに格納することで、
自動的にhtmlページを作成して公開することができます。

## Webページ
[公開しているWebページへのリンク](https://gri51.github.io/ksh_chart/ "https://gri51.github.io/ksh_chart/")

## ToDo
- CIに無理押し判定を追加
- カバレッジの改善　`（if __name == '__main__')`の中身もテスト
- Languagesの判定から.kshファイルを除外（できるか不明）
- CIに差分元パッケージダウンロード＋パス指定が正しいかの判定を追加
- CIでzip化したファイルを解凍して`kshootmania.exe`で再生できるかテスト
- 譜面紹介動画の自動生成
