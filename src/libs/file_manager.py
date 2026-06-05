from typing import Final

from chardet.universaldetector import UniversalDetector

CHARACTER_CODE_CONF_THRESHOLD: Final[float] = 0.8


def get_file_encoding(file_path: str) -> str | None:
    """UniversalDetectorを使用して文字コードを判定する。

    Parameters
    ----------
    file_path : str
        文字コードを判定したいファイルのフルパス

    Returns
    -------
    str | None
        文字コードの判定結果。判定できなかった場合、Noneを返す。
    """

    with open(file_path, 'rb') as file:
        detector = UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    # 判定結果の確認
    if detector.result['confidence'] >= CHARACTER_CODE_CONF_THRESHOLD:
        return detector.result['encoding']
    # 分析結果が怪しいので、分析失敗の意味でNoneを返す。
    return None
