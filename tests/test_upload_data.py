import unittest
import src.upload_data as ud
import os
from datetime import datetime

class TestUploadData(unittest.TestCase):
    def test_upload_data(self):
        file_path = "countries_population_area.csv"
        main_name = file_path.split(".")[0]
        uploader = ud.UploadData(file_path)
        saved_file_path = uploader.upload_data()
        self.assertTrue(os.path.exists(saved_file_path))
        expected_file_name = f"{main_name}_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        self.assertEqual(os.path.basename(saved_file_path), expected_file_name)
        os.remove(saved_file_path)


if __name__ == "__main__":
    unittest.main()
