import logging
import os
from io import BytesIO
from abc import ABC, abstractmethod
from typing import Iterable, Tuple, Type

from geometry.exceptions import StopPipelineError


logger = logging.getLogger(__name__)


class FileProcessor(ABC):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        FileProcessorRegistry().add(cls)

    @abstractmethod
    def read(self, file: BytesIO) -> BytesIO:
        pass

    @abstractmethod
    def write(self, data: bytes) -> bytes:
        pass

    @classmethod
    def get_display_name(cls):
        return cls.__name__

    @classmethod
    def is_ready(cls) -> bool:
        return True

    def __init__(self, gui):
        self.gui = gui


def read_pipeline(file, pipeline: Iterable[FileProcessor]):
    for processor in pipeline:
        try:
            file = processor.read(file)
        except StopPipelineError as e:
            logger.error(e.message)
            raise e
        except Exception as e:
            logger.exception('Unexpected error on read.')
            raise StopPipelineError(
                f'Unexpected error in the {processor.get_display_name()}.'
            ) from e

    return file


def write_pipeline(data: bytes, pipeline: Iterable[FileProcessor]):
    for processor in pipeline:
        try:
            data = processor.write(data)
        except StopPipelineError as e:
            logger.error(e.message)
            raise e
        except Exception as e:
            logger.exception('Unexpected error on write.')
            raise StopPipelineError(
                f'Unexpected error in the {processor.get_display_name()}.'
            ) from e

    return data


class FileProcessorRegistry:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Not thread-safe start.
        if cls._instance is not None:
            return cls._instance
        # Not thread-safe end.
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        # Not thread-safe start.
        if type(self)._instance is not None:
            return

        self.processor_classes = []
        type(self)._instance = self
        # Not thread-safe end.

    def add(self, processor_class: Type[FileProcessor]):
        self.processor_classes.append(processor_class)

    def get(self) -> Tuple[Type[FileProcessor]]:
        return tuple(self.processor_classes)


class DebugFileProcessor(FileProcessor):
    def read(self, file):
        file.seek(0, os.SEEK_END)
        logger.debug('Debug processor: %s bytes were read.', file.tell())
        file.seek(0)
        return file

    def write(self, data: bytes):
        logger.debug('Debug processor: going to write %s bytes.', len(data))
        return data


