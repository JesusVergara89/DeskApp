import tkinter as tk
from tkinter import filedialog, ttk
import os
from src.upload_data import UploadData
from src.data_frame_convertion import DataFrameConversion
from src.delet_files_on_files import delete_files_on_files

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cargador de CSV")

        self.selected_columns = []
        self.max_selected_columns = 4

        def combined_action():
            self.load_file()
            self.clear_selection()

        self.load_button = tk.Button(root, text="Cargar archivo CSV", command=combined_action)
        self.load_button.pack(pady=20)

        self.column_button_frame = tk.Frame(root)

        self.tree = ttk.Treeview(root)

        self.selected_columns_frame = tk.Frame(root)

        self.clear_button = tk.Button(root, text="Limpiar selección", command=self.clear_selection)

        self.data_frame = None

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_file(self):
        self.clear_files_folder()

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            uploader = UploadData(file_path)
            new_file_path = uploader.upload_data()
            print(f"Archivo CSV procesado y guardado en: {new_file_path}")

            self.df_conversion(new_file_path)

    def clear_files_folder(self):
        files_folder = 'files'
        if os.path.exists(files_folder):
            for filename in os.listdir(files_folder):
                file_path = os.path.join(files_folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(files_folder)

    def df_conversion(self, file_path):
        converter = DataFrameConversion(file_path)
        self.data_frame = converter.convert_data_frame()

        self.column_button_frame.pack(padx=10, pady=10)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        column_types = [(col, str(self.data_frame[col].dtype)) for col in self.data_frame.columns]

        for widget in self.column_button_frame.winfo_children():
            widget.destroy()

        for col, dtype in column_types:
            button = tk.Button(self.column_button_frame, text=f"{col} : {dtype}",
                               command=lambda col=col: self.select_column(col))
            button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree.delete(*self.tree.get_children())

        self.tree["columns"] = list(self.data_frame.columns)
        self.tree["show"] = "headings"

        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)

        for index, row in self.data_frame.iterrows():
            self.tree.insert("", "end", values=list(row))

    def select_column(self, column_name):
        if column_name in self.selected_columns:
            print(f"La columna {column_name} ya está seleccionada.")
            return

        if len(self.selected_columns) >= self.max_selected_columns:
            print("Ya has seleccionado el máximo número de columnas permitidas.")
            return

        self.selected_columns.append(column_name)
        print(f"Columna seleccionada: {column_name}")

        self.show_selected_columns()

        if len(self.selected_columns) >= self.max_selected_columns:
            self.clear_button.pack(pady=10)

    def show_selected_columns(self):
        for widget in self.selected_columns_frame.winfo_children():
            widget.destroy()

        self.selected_columns_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        for idx, col in enumerate(self.selected_columns):
            column_frame = tk.Frame(self.selected_columns_frame)
            column_frame.grid(row=0, column=idx, padx=10, pady=10, sticky="n")

            column_tree = ttk.Treeview(column_frame)
            column_tree.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

            column_tree["columns"] = [col]
            column_tree["show"] = "headings"
            column_tree.heading(col, text=col)
            column_tree.column(col, width=200) 

            for index, row in self.data_frame[[col]].head(5).iterrows():
                column_tree.insert("", "end", values=list(row))

            self.show_statistics(idx)


    def show_statistics(self, column_idx):
        stats_columns = ['Media', 'Varianza', 'Desviación estándar', 'Percentil 25', 'Percentil 50 (Mediana)', 'Percentil 75']
        stats_values = [''] * len(stats_columns)

        if self.data_frame is not None:
            col = self.selected_columns[column_idx]
            column_data = self.data_frame[col]
            stats_values[0] = f"{column_data.mean():.2f}"
            stats_values[1] = f"{column_data.var():.2f}"
            stats_values[2] = f"{column_data.std():.2f}"
            stats_values[3] = f"{column_data.quantile(0.25):.2f}"
            stats_values[4] = f"{column_data.quantile(0.50):.2f}"
            stats_values[5] = f"{column_data.quantile(0.75):.2f}"

        stats_frame = tk.Frame(self.selected_columns_frame)
        stats_frame.grid(row=1, column=column_idx, padx=10, pady=10, sticky="n")

        for stat_idx, stat in enumerate(stats_columns):
            label = tk.Label(stats_frame, text=stat)
            label.grid(row=stat_idx, column=0, padx=5, pady=5, sticky="w")

            value_label = tk.Label(stats_frame, text=stats_values[stat_idx])
            value_label.grid(row=stat_idx, column=1, padx=5, pady=5, sticky="w")

        self.clear_button.pack(pady=10)

    def clear_selection(self):
        self.selected_columns = []  
        self.selected_columns_frame.pack_forget() 

        for widget in self.selected_columns_frame.winfo_children():
            widget.destroy()

        self.clear_button.pack_forget()

        for child in self.selected_columns_frame.winfo_children():
            child.destroy()

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.load_button.pack(pady=20) 

    def on_close(self):
        delete_files_on_files('files')
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
