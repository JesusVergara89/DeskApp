import tkinter as tk
from tkinter import filedialog
from .upload_data import UploadData

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cargador de CSV")

        self.load_button = tk.Button(root, text="Cargar archivo CSV", command=self.load_file)
        self.load_button.pack(pady=20)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            #uploader = UploadData(f'{file_path}heheheh') #fail
            uploader = UploadData(file_path)  
            new_file_path = uploader.upload_data()  
            print(f"Archivo CSV procesado y guardado en: {new_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
