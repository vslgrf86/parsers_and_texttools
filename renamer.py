import os
import datetime

def rename_files(folder_path):
    files = [file for file in os.listdir(folder_path) if file.endswith(".mp4")]

    # Sort files based on their modification time
    files_with_time = [(file, os.path.getmtime(os.path.join(folder_path, file))) for file in files]
    files_with_time.sort(key=lambda x: x[1])

    # Rename files
    for index, (file, _) in enumerate(files_with_time, start=1):
        _, file_extension = os.path.splitext(file)
        new_name = f"{index}{file_extension}"
        
        # Rename the file
        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)

if __name__ == "__main__":
    folder_path = "/Users/vgaryfallos/Desktop/tum/1" # Change this to the path of your folder
    rename_files(folder_path)
