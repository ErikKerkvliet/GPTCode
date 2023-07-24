import json
import time
import tkinter as tk
from time import sleep
import glv
from tkinter import ttk
from Watchers.Percentages import Percentages
from Watchers.Steps import Steps


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Watcher')
        self.window.geometry('1270x600')
        self.option = ''
        self.run_time = ''
        self.data = {}
        self.treeview = {}

        self.watchers = {
            glv.WATCHER_PERCENTAGES: Percentages(),
            glv.WATCHER_STEPS: Steps(),
        }
        for exchange in glv.EXCHANGES:
            self.make_tree(exchange)

    def make_tree(self, exchange):
        # Top level Treeview object
        self.treeview[exchange] = ttk.Treeview(self.window)

        # Create a custom style for Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview')

        self.treeview[exchange] = ttk.Treeview(self.window, style='Treeview')
        style.configure("Treeview", foreground="black", background="white")

        self.treeview[exchange].pack(anchor='n', fill="both", expand=True)

        data = []
        while len(data) == 0:
            data = self.load_file(exchange)
            if len(data) == 0:
                sleep(10)

        titles = self.get_columns(list(data[0].keys()))
        self.treeview[exchange]["columns"] = titles

        self.treeview[exchange].heading("#0", text="")
        self.treeview[exchange].column("#0", width=10, stretch=False)

        for column in titles:
            heading_text = column.title()
            self.treeview[exchange].heading(column, text=heading_text)
            anchor_value = tk.E
            if column == 'code':
                column_width = 30
                anchor_value = tk.W
            elif column == 'available':
                column_width = 110
            elif column == 'difference %':
                column_width = 100
            elif column == 'sells':
                column_width = 40
            elif column in ['position', 'more ⇧', 'less ⇩']:
                column_width = 50
            else:
                column_width = 80

            self.treeview[exchange].column(column, width=column_width, anchor=anchor_value)

        self.treeview[exchange].heading("", text="")
        self.treeview[exchange].column("", width=10, stretch=False)

    def load_data(self, exchange):
        data = self.load_file(exchange)

        self.treeview[exchange].delete(*self.treeview[exchange].get_children())

        for row in data:
            for key in row.keys():
                if row[key] == glv.DEFAULT_CURRENCY:
                    continue

                row[key] = glv.convert_to_value(row[key])

            result = self.watchers[self.option].load_row(self.treeview[exchange], row)

            self.treeview[exchange].insert("", "end", text="", values=list(result['row'].values()), tags=result['tags'])

        combined_dict = data[1].copy()
        combined_dict = {key: '' for key in combined_dict}
        combined_dict[list(combined_dict.keys())[0]] = exchange
        combined_dict[list(combined_dict.keys())[1]] = self.run_time
        combined_dict.update(self.watchers[self.option].get_totals())

        tags = "total"
        self.treeview[exchange].tag_configure('total', background='#e1e1e1')

        self.treeview[exchange].insert("", "end", text="", values=list(combined_dict.values()), tags=tags)
        self.watchers[self.option].reset_totals()

    def get_columns(self, columns):
        for key, column in enumerate(columns):
            columns[key] = column.replace('_', ' ')

        if self.option == glv.WATCHER_PERCENTAGES:
            columns.append('diff €')

        if glv.CURRENT_WATCHER == glv.WATCHER_PERCENTAGES:
            columns.append('value in €')

        columns.append('')
        return columns

    def load_file(self, exchange):
        save_file = f'{glv.SAVE_FILE}_{exchange}'

        with open(save_file) as file:
            data = json.load(file)

            if data[0] == {}:
                self.option = ''
                self.run_time = ''
                return {}

            if 'option' == list(data[0].keys())[0]:
                self.option = data[0]['option']
                self.run_time = data[0]['run_time']
                del data[0]
            elif 'run_time' == list(data[0].keys())[0]:
                self.option = glv.WATCHER_STEPS
                self.run_time = data[0]['run_time']
                del data[0]
            else:
                self.option = glv.WATCHER_STEPS
                del data[0]

            file.close()
        return sorted(data, key=lambda x: x['code'])


if __name__ == "__main__":
    app = App()

    # Refresh interval in milliseconds (e.g., refresh every 1 second)
    refresh_interval_ms = glv.TIMER * 1000

    def refresh(exchanges):
        for exchange in exchanges:
            app.load_data(exchange)

        app.window.after(refresh_interval_ms, refresh, exchanges)

    # Schedule initial call and start refreshing
    app.window.after(0, refresh(glv.EXCHANGES))

    tk.mainloop()
