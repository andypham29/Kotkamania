import pandas as pd


class CSVReader:

    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def get_row(self, row_index):
        return self.df[row_index]

    def get_all_colname(self):
        return self.df.Names

    def get_col_by_colname(self, column_name):
        return self.df.get(column_name)
