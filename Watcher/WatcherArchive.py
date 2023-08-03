import glv
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class WatcherArchive:
    def __init__(self):
        self.window = tk.Tk()
        icon = Image.open("watcher.png")
        photo = ImageTk.PhotoImage(icon)
        self.window.wm_iconphoto(False, photo)
        self.window.geometry('700x400')

    def build(self, exchange, index):
        # configure the grid layout
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('tree')

        # create a treeview
        tree = ttk.Treeview(self.window, style='Treeview')
        style.configure("Treeview", foreground="black", background="white")

        tree.heading('#0', text='Crypto currencies', anchor=tk.W)

        save_file = f'{glv.SAVE_FILE}_{exchange}'
        balance = 0
        with open(save_file) as file:
            data = json.load(file)
            self.window.title(f'Watcher Hierarchical     |     Run Time: {data[0]["run_time"]}')
            balance = round(data[0]["balance_euro"], 5)
            del data[0]
        entries = list(data)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('tree')

        # create a treeview
        tree = ttk.Treeview(self.window, style='Treeview', height=400)
        style.configure("Treeview", foreground="black", background="white")

        tree.heading('#0', text=exchange, anchor=tk.W)

        # adding data
        key = 0
        for entry in entries:
            tree.insert('', tk.END, text=entry['code'], iid=str(key), open=False)
            self.insert_sub_entries(tree, entry, key)
            key += 1

        tree.heading('amount', text=f'€ {balance}', anchor=tk.W)

        # place the Treeview widget on the root window
        tree.grid(row=0, column=index, sticky=tk.NW)

    def insert_sub_entries(self, tree, entry, base_key):
        key = base_key + 1
        del entry['code']
        tree['columns'] = ['name', 'amount']
        for col_key in reversed(list(entry.keys())):
            name = f'{col_key.capitalize()}'
            amount = f'{"" if entry[col_key] is None else f"{float(entry[col_key]):.8f}".rstrip("0").strip(".")}'

            row = {
                'name': name,
                'amount': amount
            }
            tree.column("#0", width=100, stretch=False)
            tree.column('name', width=100, anchor=tk.W)
            tree.column('amount', width=150, anchor=tk.W)
            # tree.column('', width=50, anchor=tk.W)
            tree.insert('', tk.END, values=list(row.values()), iid=f'{base_key}_{key}', open=False)
            tree.move(f'{base_key}_{key}', base_key, 0)
            key += 1
        return key


if __name__ == '__main__':
    watcher_archive = WatcherArchive()

    # Refresh interval in milliseconds (e.g., refresh every 1 second)
    refresh_interval_ms = glv.TIMER * 1000

    def refresh(exchanges):
        for index, exchange in enumerate(exchanges):
            watcher_archive.build(exchange, index)

        watcher_archive.window.after(refresh_interval_ms, refresh, exchanges)

    # Schedule initial call and start refreshing
    watcher_archive.window.after(0, refresh(glv.EXCHANGES))

    tk.mainloop()
