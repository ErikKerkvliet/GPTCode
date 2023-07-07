import source.globalvar as globalvar


class PercentagesWatcher:
    def load_data(self, treeview, row):
        for key in row.keys():
            row[key] = globalvar.convert_to_value(row[key])

        tags = "odd row"
        treeview.tag_configure('oddrow', background='white')

        if row['rate'] > row['buy_rate'] and row['amount'] != 0:
            tags = "higher"
            treeview.tag_configure('higher', background='#b4f9ab')

        if row['rate'] < row['buy_rate']:
            tags = "less"
            treeview.tag_configure('less', background='#f59f9f')

        if row['rate'] < (row['buy_rate'] * 0.99):
            tags = "lesser"
            treeview.tag_configure('lesser', background='#ff4141')

        if row['rate'] > (row['buy_rate'] * 1.01) and row['amount'] != 0:
            tags = "profit"
            treeview.tag_configure('profit', background='#44a448')

        for key in row:
            try:
                if row[key] == 0:
                    row[key] = '0'
                elif row[key] % 1 == 0:
                    row[key] = row[key]
                elif row[key] < 0.000009:
                    row[key] = row[key]
            except Exception:
                pass

        row['profit'] = f'{row["profit"]:.8f}' if int(row["profit"]) > 0 else 0
        row['diff'] = f'{float(row["rate"]) - float(row["buy_rate"]):.8f}' \
            if float(row["rate"]) - float(row["buy_rate"]) > 0 else 0
        row['diff €'] = f'{(row["rate"] / row["buy_rate"]):.8f}' if int(row["buy_rate"]) > 0 else 0

        treeview.insert("", "end", text="", values=list(row.values()))