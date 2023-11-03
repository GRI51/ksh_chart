import logging
import logging.handlers
import os


def set_logger(module_name: str, log_dir: str | None = None) -> logging.Logger:
    """loggingモジュールのロガーを取得する。
    コンソールにはINFO以上のメッセージを表示し、
    ログファイルにはDEBUG以上のメッセージを表示する。
    ログファイルは1ファイル当り10MBまで。
    直近９個のファイルのみ保持し、それより過去のファイルは自動削除される。

    Parameters
    ----------
    module_name : str
        モジュール名。ここで指定した名称が、ログメッセージに表示される。
        （例）
        logger = python_logger.set_logger('module_name')
        logger.info('ログメッセージ。')
        > 
    log_dir : str | None
        ログファイルの出力先フォルダ。
        Noneを指定すると、src直下のlogsフォルダが出力先になる。

    Returns
    -------
    logging.Logger
        作成したロガー
    """
    logger = logging.getLogger(module_name)
    logger.handlers.clear()
    # コンソール表示用のハンドラー作成
    stream_handler = logging.StreamHandler()
    # ログファイル出力用のハンドラーとログファイル出力先を作成
    if log_dir is None:
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    LOG_FILE_NAME = 'logfile.log'
    file_handler = logging.handlers.RotatingFileHandler(os.path.join(
        log_dir, LOG_FILE_NAME), maxBytes=int(10e6), backupCount=9)
    # フォーマット設定
    stream_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    stream_handler.setFormatter(stream_formatter)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] (%(filename)s | %(funcName)s | %(lineno)s) %(message)s")
    file_handler.setFormatter(file_formatter)
    # 表示する最低レベル
    logger.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)
    # ハンドラーを設定
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    # 作成したロガーを返却
    return logger
