import logging
import logging.handlers
import os
import pickle
import socketserver
import struct
from typing import Any

LOG_FILE_NAME = 'logfile.log'
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')


def set_logger(module_name: str, log_dir: str | None = None, multiprocess: bool = False) -> logging.Logger:
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
        > 2023-11-04 15:55:00,954 [INFO] (module_name | <func_name> | 26) ログメッセージ。
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
        log_dir = LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    if multiprocess:
        file_handler = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        # 通信量を減らすため、ここでの伝播は行わない。
        logger.propagate = False
    else:
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


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """ LogRecordバイナリを読み込んで処理する。 """

    # ロガーを保存しておく。
    loggers = {}

    def handle(self) -> None:
        """ バイナリからLogRecordオブジェクトを作成し処理する。 """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data: bytes) -> dict:
        """ バイナリ化されたデータを元のオブジェクトに変換する。 """
        return pickle.loads(data)

    def handleLogRecord(self: socketserver.StreamRequestHandler, record: logging.LogRecord) -> None:
        """ LogRecordオブジェクトを処理する。 """
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name

        # 公式コードに追加した部分。すでにロガーが存在していれば既存のものを使う。
        if name in self.loggers:
            logger = self.loggers[name]
        else:
            logger = logging.getLogger(name)
            handler = logging.handlers.RotatingFileHandler(os.path.join(
                LOG_DIR, LOG_FILE_NAME), maxBytes=int(10e6), backupCount=9)
            logger.addHandler(handler)
            logger.propagate = True
            self.loggers[name] = logger

        logger.handle(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """ ログを受け取るソケットサーバー。 """

    allow_reuse_address = True

    def __init__(self, host: str = 'localhost', port: int = logging.handlers.DEFAULT_TCP_LOGGING_PORT, handler: Any = LogRecordStreamHandler) -> None:
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self) -> None:
        """ ソケットが読み込み可能になるまで待機する。 """
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort


def main() -> None:
    tcpserver = LogRecordSocketReceiver()
    print('About to start TCP server...')
    tcpserver.serve_until_stopped()


if __name__ == '__main__':
    main()
