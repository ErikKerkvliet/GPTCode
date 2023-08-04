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

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('tree')

        # create a treeview
        style.configure("Treeview", foreground="black", background="white")

        self.trees = {}
        for exchange in glv.EXCHANGES:
            self.trees[exchange] = ttk.Treeview(self.window, style='Treeview', height=400)

    def build(self, exchange, index):
        # configure the grid layout
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        item_states = {}
        for item_id in self.trees[exchange].get_children():
            item_states[item_id] = self.trees[exchange].item(item_id, 'open')

        self.trees[exchange].heading('#0', text='Crypto currencies', anchor=tk.W)

        save_file = f'{glv.SAVE_FILE}_{exchange}'

        with open(save_file) as file:
            data = json.load(file)
            self.window.title(f'Watcher Hierarchical')
            balance = round(data[0]["balance_euro"], 5)
            run_time = data[0]["run_time"]
            del data[0]
        entries = list(data)

        self.trees[exchange].delete(*self.trees[exchange].get_children())
        self.trees[exchange].heading('#0', text=exchange)

        # adding data
        key = 0

        self.trees[exchange].tag_configure('green', background='#e9ffe9')
        self.trees[exchange].tag_configure('red', background='#ffece9')
        self.trees[exchange].tag_configure('white', background='white')
        for entry in entries:
            state = False if item_states == {} else item_states[str(key)]
            if entry['rate'] == entry['buy_rate']:
                tag = ('white',)
            else:
                tag = ('green',) if entry['rate'] > entry['buy_rate'] else ('red',)
            self.trees[exchange].insert('', tk.END, text=entry['code'], iid=str(key), open=state, tags=tag)
            self.insert_sub_entries(self.trees[exchange], entry, key)
            key += 1

        self.trees[exchange].heading('name', text=run_time)
        self.trees[exchange].heading('amount', text=f'€ {balance}')

        # place the Treeview widget on the root window
        self.trees[exchange].grid(row=0, column=index, sticky=tk.NW)

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
