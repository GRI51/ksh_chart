from chardet.universaldetector import UniversalDetector


def get_file_encoding(file_path) -> str | None:
    with open(file_path, 'rb') as file:
        detector = UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    if detector.result['confidence'] < 0.8:
        return None
    else:
        return detector.result['encoding']
