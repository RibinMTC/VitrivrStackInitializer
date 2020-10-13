import json


class ServerConfigData:
    server_content_base_path_str = ""
    thumbnails_base_path_str = ""
    cineast_base_path_str = ""
    cineast_job_file_str = ""
    cineast_job_file_path_str = ""
    cottontail_base_path_str = ""
    vitrivr_ng_base_path_str = ""

    def __init__(self):
        with open("../vitrivr_paths_config_new.json") as json_paths_file:
            data = json.load(json_paths_file)
            self.server_content_base_path_str = data['content_base']
            self.thumbnails_base_path_str = data['thumbnails_base']
            self.cineast_base_path_str = data['cineast_base']
            self.cineast_job_file_str = data['cineast_job_file']
            self.cineast_job_file_path_str = self.cineast_base_path_str + '/' + self.cineast_job_file_str
            self.cottontail_base_path_str = data['cottontail_base']
            self.vitrivr_ng_base_path_str = data['vitrivr_ng_base']
