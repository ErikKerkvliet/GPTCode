import json
import tkinter as tk
from time import sleep
import globalvar
from tkinter import ttk
from WatcherOptions.Percentages import PercentagesWatcher
from WatcherOptions.Steps import StepsWatcher

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Watcher')
        self.window.geometry('1467x100')

        self.watcher_options = {
            'percentages': PercentagesWatcher(),
            'steps': StepsWatcher(),
        }

        self.data = []
        while len(self.data) == 0:
            self.data = self.load_file()
            if len(self.data) == 0:
                sleep(10)

        # Top level Treeview object
        self.treeview = ttk.Treeview(self.window)

        # Columns (treeview objects also)
        columns = self.get_columns(list(self.data[0].keys()))

        # Create a custom style for Treeview
        style = ttk.Style()
        style.theme_use('clam')

        self.treeview = ttk.Treeview(self.window, style='Treeview')

        self.treeview.pack(fill="both", expand=True)

        self.data = []
        while len(self.data) == 0:
            self.data = self.load_file()
            if len(self.data) == 0:
                sleep(10)

        titles = self.get_columns(list(self.data[0].keys()))
        self.treeview["columns"] = titles

        self.treeview.heading("#0", text="")
        self.treeview.column("#0", width=10, stretch=False)

        for index, column in enumerate(titles):
            heading_text = column.title()
            self.treeview.heading(column, text=heading_text)

            anchor_value = tk.E
            if index == 0:
                column_width = 60
                anchor_value = tk.W
            elif column == 'available':
                column_width = 110
            elif column == 'sells':
                column_width = 70
            else:
                column_width = 100

            self.treeview.column(column, width=column_width, anchor=anchor_value)

        self.treeview.heading("", text="")
        self.treeview.column("", width=10, stretch=False)

    def load_data(self):
        self.data = None
        self.data = self.load_file()

        self.treeview.delete(*self.treeview.get_children())

        for row in self.data:
            result = self.watcher_options[globalvar.OPTION].load_row(self.treeview, row)

            self.treeview.insert("", "end", text="", values=list(result['row'].values()), tags=result['tags'])

    @staticmethod
    def get_columns(columns):
        for key, column in enumerate(columns):
            columns[key] = column.replace('_', ' ')

        if globalvar.OPTION == 'percentages':
            columns.append('diff')
            columns.append('diff €')
        columns.append('')
        return columns

    @staticmethod
    def load_file():
        with open('./save') as file:
            data = json.load(file)
            file.close()
        return sorted(data, key=lambda x: x['code'])


if __name__ == "__main__":
    app = App()

    # Refresh interval in milliseconds (e.g., refresh every 1 second)
    refresh_interval_ms = 5000

    def refresh():
        app.load_data()

        app.window.after(refresh_interval_ms, refresh)

    # Schedule initial call and start refreshing
    app.window.after(refresh_interval_ms, refresh)

    tk.mainloop()
