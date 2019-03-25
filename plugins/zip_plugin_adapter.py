import logging
from io import BytesIO
from geometry.file_processor import FileProcessor


logger = logging.getLogger(__name__)


def _find_original_class():
    that_one_class = [x for x in object.__subclasses__() if x.__name__ == 'ZipPlugin']
    if len(that_one_class) != 1:
        return None

    return that_one_class[0]


class ZipPluginAdapter(FileProcessor):

    _adaptee_class = None

    @classmethod
    def get_adaptee_class(cls):
        if cls._adaptee_class is None:
            cls._adaptee_class = _find_original_class()

        return cls._adaptee_class

    @classmethod
    def get_display_name(cls):
        return 'ZipPlugin'

    @classmethod
    def is_ready(cls):
        return cls.get_adaptee_class() is not None

    def __init__(self, gui):
        super().__init__(gui)
        self._adaptee =  self.get_adaptee_class()()

    def write(self, data: bytes):
        return self._adaptee.zip(data)

    def read(self, file: BytesIO) -> BytesIO:
        try:
            return BytesIO(self._adaptee.unzip(file.read()))
        except OSError:
            logger.warning("It looks like the file wasn't compressed.")
            file.seek(0)
            return file
