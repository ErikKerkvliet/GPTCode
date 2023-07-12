import json
import tkinter as tk
from time import sleep
import globalvar
from tkinter import ttk
from Watchers.Percentages import Percentages
from Watchers.Steps import Steps


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Watcher')
        self.window.geometry('1270x200')
        self.option = ''
        self.run_time = ''

        self.watchers = {
            globalvar.WATCHER_PERCENTAGES: Percentages(),
            globalvar.WATCHER_STEPS: Steps(),
        }

        self.data = []
        while len(self.data) == 0:
            self.data = self.load_file()
            if len(self.data) == 0:
                sleep(10)

        # Top level Treeview object
        self.treeview = ttk.Treeview(self.window)

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

        for column in titles:
            heading_text = column.title()
            self.treeview.heading(column, text=heading_text)
            anchor_value = tk.E
            if column == 'code':
                column_width = 30
                anchor_value = tk.W
            elif column == 'available':
                column_width = 110
            elif column == 'difference %':
                column_width = 110
            elif column == 'sells':
                column_width = 40
            elif column in ['position', 'more ⇧', 'less ⇩']:
                column_width = 50
            else:
                column_width = 80

            self.treeview.column(column, width=column_width, anchor=anchor_value)

        self.treeview.heading("", text="")
        self.treeview.column("", width=10, stretch=False)

    def load_data(self):
        self.data = self.load_file()

        self.treeview.delete(*self.treeview.get_children())

        for row in self.data:
            for key in row.keys():
                if row[key] == globalvar.DEFAULT_CURRENCY:
                    continue

                row[key] = globalvar.convert_to_value(row[key])

            result = self.watchers[self.option].load_row(self.treeview, row)

            self.treeview.insert("", "end", text="", values=list(result['row'].values()), tags=result['tags'])

        combined_dict = self.data[1].copy()
        combined_dict = {key: '' for key in combined_dict}
        combined_dict[list(combined_dict.keys())[0]] = self.run_time
        combined_dict.update(self.watchers[self.option].get_totals())

        self.treeview.insert("", "end", text="", values=list(combined_dict.values()))
        self.watchers[self.option].reset_totals()

    def get_columns(self, columns):
        for key, column in enumerate(columns):
            columns[key] = column.replace('_', ' ')

        if self.option == globalvar.WATCHER_PERCENTAGES:
            columns.append('diff €')

        if globalvar.CURRENT_WATCHER == globalvar.WATCHER_PERCENTAGES:
            columns.append('value in €')

        columns.append('')
        return columns

    def load_file(self):
        with open(globalvar.SAVE_FILE) as file:
            data = json.load(file)

            if 'option' == list(data[0].keys())[0]:
                self.option = data[0]['option']
                self.run_time = data[0]['run_time']
                del data[0]
            else:
                self.option = globalvar.WATCHER_STEPS

            file.close()
        return sorted(data, key=lambda x: x['code'])


if __name__ == "__main__":
    app = App()

    # Refresh interval in milliseconds (e.g., refresh every 1 second)
    refresh_interval_ms = globalvar.TIMER * 1000

    def refresh():
        app.load_data()

        app.window.after(refresh_interval_ms, refresh)

    # Schedule initial call and start refreshing
    app.window.after(refresh_interval_ms, refresh)

    tk.mainloop()
