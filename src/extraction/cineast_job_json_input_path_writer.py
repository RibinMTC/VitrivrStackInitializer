import json


def __update_json_file(new_import_path_str, cineast_job_file_path_str):
    with open(cineast_job_file_path_str, 'r') as json_file:
        data = json.load(json_file)
        if 'input' not in data:
            raise ValueError("No property -input- found in the provided json! Aborting process")
        if 'path' not in data['input']:
            raise ValueError("No property -path- found in the provided json! Aborting process")

    data['input']['path'] = new_import_path_str

    with open(cineast_job_file_path_str, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def write_new_import_path_to_job_file(new_import_path_str, cineast_job_file_path_str):
    __update_json_file(new_import_path_str, cineast_job_file_path_str)
