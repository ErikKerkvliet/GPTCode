import source.globalvar as globalvar


class StepsWatcher:
    @staticmethod
    def load_row(treeview, row):
        for key in row.keys():
            row[key] = globalvar.convert_to_value(row[key]) if row[key] else 0

        tags = "odd row"
        treeview.tag_configure('oddrow', background='white')

        if row['rate'] > row['last_rate']:
            tags = "higher"
            treeview.tag_configure('higher', background='#b4f9ab')

        if row['rate'] < row['last_rate']:
            tags = "less"
            treeview.tag_configure('less', background='#ffe5e5')

        # if row['rate'] > row['buy_rate']:
        #     tags = "higher"
        #     treeview.tag_configure('higher', background='#b4f9ab')
        #
        # if row['rate'] < row['buy_rate']:
        #     tags = "less"
        #     treeview.tag_configure('less', background='#f59f9f')

        row['rate'] = f'{float(row["rate"]):.8f}'
        row['last_rate'] = f'{float(row["last_rate"]):.8f}'
        row['buy_rate'] = f'{float(row["buy_rate"]):.8f}'

        return {
            'row': row,
            'tags': tags,
        }
