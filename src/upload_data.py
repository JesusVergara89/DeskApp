import pandas as pd
import os
from datetime import datetime

class UploadData: 
    def __init__(self, file_path):
        self.file_path = file_path 

    def upload_data(self): 
        df = pd.read_csv(self.file_path)
        file_name = os.path.basename(self.file_path)
        if not os.path.exists('files'):
            os.makedirs('files')

        current_date = datetime.now().strftime('%Y-%m-%d')
        new_file_name = file_name.split(".")[0]
        new_file_name = f"{new_file_name}_data_{current_date}.csv"
        
        new_file_path = os.path.join('files', new_file_name)
        
        df.to_csv(new_file_path, index=False)
        
        return new_file_path


