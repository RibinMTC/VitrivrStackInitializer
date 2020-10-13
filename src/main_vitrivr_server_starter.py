import sys
import time

from src.utils.server_config_data import ServerConfigData
from src.utils.subprocess_communication import run_subprocess, communicate_and_log_process_output, terminate_subprocess, \
    open_log_file, close_log_file

serverConfigData = ServerConfigData()

# # ---------- START VITRIVR-NG UI ---------------#

vitrivr_ng_start_cmd = "ng serve"
vitrivr_ng_log_path = 'logs/vitrivr_ng_ui_log.txt'
vitrivr_ng_log_file = open_log_file(vitrivr_ng_log_path)

vitrivr_ng_process = run_subprocess(vitrivr_ng_start_cmd, serverConfigData.vitrivr_ng_base_path_str, log_file=vitrivr_ng_log_file)

# ---------- START COTTONTAIL DB ---------------#

cottontail_start_cmd = "java -jar build/libs/cottontaildb-1.0-SNAPSHOT-all.jar config.json"
cottontail_log_path = "logs/cottontail_log.txt"
cottontail_log_file = open_log_file(cottontail_log_path)

cottontail_process = run_subprocess(cottontail_start_cmd, serverConfigData.cottontail_base_path_str, log_file=cottontail_log_file)

# # ---------- START CINEAST ---------------#

cineast_start_cmd = "java -jar cineast-api/build/libs/cineast-api-3.0.1-full.jar cineast.json"

cineast_log_file_path = "logs/cineast_log.txt"
cineast_log_file = open_log_file(cineast_log_file_path)

# cineast should wait until the db is initialized
time.sleep(2)
cineast_process = run_subprocess(cineast_start_cmd, serverConfigData.cineast_base_path_str, log_file=cineast_log_file)

server_terminate_cmd = "stop"
try:
    while True:
        user_input = input("Enter * stop * to terminate server\n")
        if user_input == server_terminate_cmd:
            break

except:
    print("An exception occurred: " + str(sys.exc_info()[0]))
finally:
    close_log_file(vitrivr_ng_log_file)
    close_log_file(cineast_log_file)
    close_log_file(cottontail_log_file)

    terminate_subprocess(vitrivr_ng_process)
    vitrivr_ng_process.communicate()

    cineast_process.communicate()
    cottontail_process.communicate()
