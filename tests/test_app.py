import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from src.app import App 

class TestApp(unittest.TestCase):

    @patch('src.app.filedialog.askopenfilename')  
    @patch('src.app.UploadData')  
    def test_load_file(self, MockUploadData, MockAskOpenFilename):
        MockAskOpenFilename.return_value = 'test_data.csv'

        mock_uploader = MagicMock()
        mock_uploader.upload_data.return_value = 'processed_data.csv'
        MockUploadData.return_value = mock_uploader

        root = tk.Tk()
        app = App(root)

        app.load_file()

        MockAskOpenFilename.assert_called_once_with(filetypes=[("CSV files", "*.csv")])
        
        MockUploadData.assert_called_once_with('test_data.csv')

        mock_uploader.upload_data.assert_called_once()

        with patch('builtins.print') as mocked_print:
            app.load_file()
            mocked_print.assert_called_once_with("Archivo CSV procesado y guardado en: processed_data.csv")

if __name__ == "__main__":
    unittest.main()
