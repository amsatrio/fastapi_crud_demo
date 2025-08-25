
import base64
import logging
import os
from pathlib import Path
import shutil


log = logging.getLogger(__name__)
def read_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            return base64.b64encode(file_content).decode('utf-8')
    except FileNotFoundError:
        log.error(f"Error: File '{file_path}' not found.")
    except Exception as e:
        log.error(f"An error occurred: {e}")
    return None

def write_file(file, base_path, file_id, file_type, file_name):
    path_dir = base_path + "/" + str(file_id) + "/" + file_type
    log.info("path: " + path_dir)
    os.makedirs(path_dir, exist_ok=True)
    destination = Path(path_dir + "/" + str(file_name))
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file, buffer)
        return destination
    except Exception as e:
        log.error(f"An error occurred: {e}")
    finally:
        file.close()
    return None

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"File '{file_path}' not found.")