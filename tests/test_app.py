import unittest
from unittest.mock import patch, MagicMock
from src.app import App

class TestApp(unittest.TestCase):

    @patch('src.app.filedialog.askopenfilename')
    @patch('src.app.UploadData')
    def test_load_file(self, MockUploadData, MockAskOpenFilename):
        # Configurar el valor devuelto por askopenfilename
        MockAskOpenFilename.return_value = 'test_data.csv'

        # Configurar el comportamiento del mock de UploadData
        mock_uploader = MagicMock()
        mock_uploader.upload_data.return_value = 'processed_data.csv'
        MockUploadData.return_value = mock_uploader

        # Simular la instancia de la aplicación sin crear una ventana real
        with patch('src.app.tk.Tk') as MockTk:
            mock_root = MagicMock()
            MockTk.return_value = mock_root
            app = App(mock_root)

            # Ejecutar el método load_file
            app.load_file()

            # Verificar que se llamó a askopenfilename
            MockAskOpenFilename.assert_called_once_with(filetypes=[("CSV files", "*.csv")])

            # Verificar que UploadData fue llamado con el archivo correcto
            MockUploadData.assert_called_once_with('test_data.csv')

            # Verificar que upload_data fue llamado
            mock_uploader.upload_data.assert_called_once()

            # Verificar la salida esperada
            with patch('builtins.print') as mocked_print:
                app.load_file()
                mocked_print.assert_called_once_with("Archivo CSV procesado y guardado en: processed_data.csv")
