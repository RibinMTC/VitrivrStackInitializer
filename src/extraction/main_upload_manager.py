"""
This script is responsible for the following tasks:
    1. The provided user content(path to content) is stored to the server file system
    2. The newly stored folder in the server is written as input to the cineast extraction job json file
    3. Finally, the extraction is performed by cineast using the new job file
"""
import argparse
from pathlib import Path
import os
import sys

from src.extraction.ml_predictor_server_manager import start_ml_predictor_server

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extraction.cineast_job_json_input_path_writer import write_new_import_path_to_job_file
from src.extraction.cineast_to_db_extraction import extract_content_to_database
from src.utils.server_config_data import ServerConfigData
from src.extraction.user_images_to_server_storer import store_user_content_to_server


def read_args():
    parser = argparse.ArgumentParser(description='Uploads a given folder of content to the server')

    parser.add_argument('--content_folder', type=str, help='The folder path containing the content for ML-Prediction')

    parser.add_argument('--first_extraction', default=False, action='store_true',
                        help='Add this flag to indicate first extraction. If set, cineast will perform a setup before '
                             'extraction')

    args = parser.parse_args()

    return args.content_folder, args.first_extraction


def __get_content_folder_path(content_folder_path_str):
    content_folder_path = Path(content_folder_path_str)
    if not content_folder_path.exists() or not any(content_folder_path.iterdir()):
        print("Aborting Upload: User folder either does not exist or is empty!")
        return None

    return content_folder_path


serverConfigData = ServerConfigData()

# 1. Start Main ml predictor server
ml_main_server_process = start_ml_predictor_server(serverConfigData.main_ml_predictor_server_script)

# 2. Read user content folder and copy the content to the server file structure
_content_folder_path, first_extraction = read_args()
_user_content_folder_path = Path(_content_folder_path)

_new_import_folder_path = store_user_content_to_server(_user_content_folder_path,
                                                       Path(serverConfigData.server_content_base_path_str))

# 3. Write new import folder path as input to the cineast json file
write_new_import_path_to_job_file(str(_new_import_folder_path), serverConfigData.cineast_job_file_path_str)

# 4. Perform extraction via cineast to cottontail db using the job file with the new import path

print("Extraction in progress...")
extract_content_to_database(serverConfigData.cottontail_base_path_str, serverConfigData.cineast_base_path_str,
                            serverConfigData.cineast_job_file_str, setup=first_extraction)

ml_main_server_process.terminate(True)
