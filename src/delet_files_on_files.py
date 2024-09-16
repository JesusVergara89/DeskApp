import os

def delete_files_on_files(files_folder):
    if os.path.exists(files_folder):
        for filename in os.listdir(files_folder):
            file_path = os.path.join(files_folder, filename)
            # Verificar si el archivo tiene una extensión .txt o .csv
            if os.path.isfile(file_path) and (filename.endswith('.txt') or filename.endswith('.csv')):
                os.remove(file_path)
                print(f"Archivo eliminado: {filename}")