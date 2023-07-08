

class Steps:
    @staticmethod
    def load_row(treeview, row):

        tags = "color"
        treeview.tag_configure('color', background='white')

        if row['rate'] > row['last_rate']:
            tags = "higher"
            treeview.tag_configure('higher', background='#b4f9ab')

        if row['rate'] < row['last_rate']:
            tags = "lesser"
            treeview.tag_configure('lesser', background='#ffe5e5')

        profit = f'{float(row["profit"]):.8f}'
        if '.' in profit:
            profit = profit.rstrip('0').strip('.')

        row['profit'] = profit
        row['rate'] = f'{float(row["rate"]):.8f}'
        row['last_rate'] = f'{float(row["last_rate"]):.8f}'
        row['top_rate'] = f'{float(row["top_rate"]):.8f}'
        row['buy_rate'] = f'{float(row["buy_rate"]):.8f}'
        row['amount_€'] = f'{float(row["amount_€"]):.4f}'

        return {
            'row': row,
            'tags': tags,
        }
