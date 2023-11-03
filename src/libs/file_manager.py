from chardet.universaldetector import UniversalDetector


def get_file_encoding(file_path: str) -> str | None:
    # UniversalDetectorを使用して文字コードを判定
    with open(file_path, 'rb') as file:
        detector = UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    # 判定結果の確認
    if detector.result['confidence'] >= 0.8:
        return detector.result['encoding']
    else:
        # 分析結果が怪しいので、分析失敗の意味でNoneを返す。
        return None
