import tkinter as tk
from geometry.file_processor import FileProcessorRegistry


class SettingsWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui()


    def _build_ui(self):
        label = tk.Label(self, text='Data pipeline:')
        label.pack(side=tk.TOP)

        checked = []

        for processor_class in FileProcessorRegistry().get():
            line = tk.Frame(self)
            line.pack(side=tk.TOP)

            checked.append(tk.IntVar())

            tk.Checkbutton(
                line,
                variable=checked[-1],
                command=self.on_pipeline_click
            ).pack(side=tk.LEFT)
            tk.Label(line, text=processor_class.get_display_name()).pack(side=tk.LEFT)

        line = tk.Frame(self)
        line.pack(side=tk.TOP)
        tk.Button(line, text='Cancel').pack(side=tk.LEFT)
        tk.Button(line, text='Ok').pack(side=tk.LEFT)

    def on_pipeline_click(self):
        pass



