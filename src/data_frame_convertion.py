import pandas as pd

class DataFrameConversion:
    def __init__(self, file_path):
        self.file_path = file_path

    def convert_data_frame(self):
        df = pd.read_csv(self.file_path)
        return df
