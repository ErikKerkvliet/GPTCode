

class Steps:
    def __init__(self):
        self.totals = {
            'sells': 0,
            'amount_€': 0,
            'profit': 0,
            'profit_€': 0,
        }

    def load_row(self, treeview, row):
        self.add_to_totals(row)

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

        difference = f'{float(row["difference"]):.8f}'
        if '.' in difference:
            difference = difference.rstrip('0').strip('.')

        profit_euro = row["profit_€"]
        # if '.' in profit_euro:
        #     profit_euro = profit_euro.rstrip('0').strip('.')

        row['profit'] = profit
        row['profit_€'] = profit_euro
        row['rate'] = f'{float(row["rate"]):.8f}'
        row['last_rate'] = f'{float(row["last_rate"]):.8f}'
        row['top_rate'] = f'{float(row["top_rate"]):.8f}'
        row['buy_rate'] = f'{float(row["buy_rate"]):.8f}'
        row['amount_€'] = f'{float(row["amount_€"]):.4f}'
        row['difference'] = difference
        row['difference_%'] = f'{float(row["difference_%"]):.8f}'.rstrip('0').strip('.')

        return {
            'row': row,
            'tags': tags,
        }

    def add_to_totals(self, row):
        for cell in row.keys():
            if cell in self.totals.keys():
                self.totals[cell] += float(row[cell])

    def get_totals(self) -> dict:
        for total in self.totals.keys():
            total_str = f'{float(self.totals[total]):.8f}'
            if '.' in total_str:
                total_str = total_str.rstrip('0').strip('.')
            self.totals[total] = total_str
        return self.totals

    def reset_totals(self):
        self.totals = {key: 0 for key in self.totals}

