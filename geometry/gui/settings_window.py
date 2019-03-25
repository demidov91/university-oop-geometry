import logging
import tkinter as tk
from functools import partial
from typing import Type, List, Callable

from geometry.file_processor import FileProcessorRegistry, FileProcessor


logger = logging.getLogger(__name__)


class SettingsWindow(tk.Toplevel):
    def __init__(
            self,
            *args,
            file_pipeline: List[Type[FileProcessor]],
            on_save: Callable,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._pipeline = file_pipeline
        self._on_save = on_save
        self._file_pipeline_class_to_index_label = {}
        self._build_ui()

    def _update_pipeline_indices(self):
        for processor_class, label in self._file_pipeline_class_to_index_label.items():
            if not processor_class in self._pipeline:
                text = ''
            else:
                text = f'({self._pipeline.index(processor_class) + 1})'

            label.config(text=text)


    def _build_ui(self):
        label = tk.Label(self, text='Data pipeline:')
        label.pack(side=tk.TOP)

        for processor_class in FileProcessorRegistry().get():
            if not processor_class.is_ready():
                continue

            line = tk.Frame(self)
            line.pack(side=tk.TOP)

            checked = tk.IntVar(value=1 if processor_class in self._pipeline else 0)

            tk.Checkbutton(
                line,
                variable=checked,
                command=partial(
                    self.on_pipeline_click,
                    processor_class,
                    checked
                )
            ).pack(side=tk.LEFT)
            tk.Label(line, text=processor_class.get_display_name()).pack(side=tk.LEFT)

            index_label = tk.Label(line, text='')
            index_label.pack(side=tk.LEFT, padx=(15, 0))
            self._file_pipeline_class_to_index_label[processor_class] = index_label

        line = tk.Frame(self)
        line.pack(side=tk.TOP)
        tk.Button(
            line,
            text='Cancel',
            command=self.destroy
        ).pack(side=tk.LEFT)
        tk.Button(
            line,
            text='Ok',
            command=self.on_save_click,
        ).pack(side=tk.LEFT)
        self._update_pipeline_indices()

    def on_pipeline_click(self, processor_class: Type[FileProcessor], is_checked: tk.IntVar):
        if is_checked.get():
            if processor_class in self._pipeline:
                logger.warning('Something went wrong. %s is added twice.', processor_class)
            else:
                self._pipeline.append(processor_class)
        else:
            if processor_class not in self._pipeline:
                logger.warning('Something went wrong. %s is already removed.', processor_class)
            else:
                self._pipeline.remove(processor_class)

        self._update_pipeline_indices()

    def on_save_click(self):
        self._on_save(self._pipeline)
        self.destroy()



