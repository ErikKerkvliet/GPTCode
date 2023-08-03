import glv
import json
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class WatcherArchive:
    def __init__(self):
        pass

    def build(self):
        # create root window
        root = tk.Tk()
        root.title('Treeview - Hierarchical Data')
        root.geometry('600x400')

        # configure the grid layout
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('tree')

        # create a treeview
        tree = ttk.Treeview(root, style='Treeview')
        style.configure("Treeview", foreground="black", background="white")

        tree.heading('#0', text='Crypto currencies', anchor=tk.W)

        save_file = f'{glv.SAVE_FILE}_Bitpanda'

        with open(save_file) as file:
            data = json.load(file)
            del data[0]
        entries = list(data)

        # adding data
        key = 0
        for entry in entries:
            tree.insert('', tk.END, text=entry['code'], iid=key, open=False)
            self.insert_sub_entries(tree, entry, key)
            key += 1

        # place the Treeview widget on the root window
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # run the app
        root.mainloop()

    def insert_sub_entries(self, tree, entry, base_key):
        key = base_key + 1
        for col_key in reversed(list(entry.keys())):
            value = f'{col_key.capitalize()}: {"" if not entry[col_key] else entry[col_key]}'
            tree.insert('', tk.END, text=value, iid=f'{base_key}_{key}', open=False)
            tree.move(f'{base_key}_{key}', base_key, 0)
            key += 1
        return key


if __name__ == '__main__':
    watcher_archive = WatcherArchive()

    watcher_archive.build()
