import time

from src.utils.subprocess_communication import open_log_file, close_log_file, run_subprocess, run_command_on_subprocess


# ---------- START COTTONTAIL DB ---------------#

def __start_cottontail(cottontail_base_path_str, cottontail_log_file):
    cottontail_start_cmd = "java -jar build/libs/cottontaildb-1.0-SNAPSHOT-all.jar " \
                           "config.json"

    cottontail_process = run_subprocess(cmd=cottontail_start_cmd, cmd_dir=cottontail_base_path_str, shell=False,
                                        log_file=cottontail_log_file)

    return cottontail_process


# ---------- START CINEAST ---------------#

def __start_cineast(cineast_base_path_str, cineast_log_file):
    cineast_start_cmd = "java -jar cineast-api/build/libs/cineast-api-3.0.1-full.jar cineast.json"

    time.sleep(2)
    cineast_process = run_subprocess(cmd=cineast_start_cmd, cmd_dir=cineast_base_path_str, shell=False,
                                     log_file=cineast_log_file)

    return cineast_process


def __extract_from_cineast(cineast_process, cineast_job_file_str, setup):
    if setup:
        run_command_on_subprocess(cineast_process, "setup --extraction " + cineast_job_file_str)
    run_command_on_subprocess(cineast_process, "extract --extraction " + cineast_job_file_str)


def extract_content_to_database(cottontail_base_path_str, cineast_base_path_str, cineast_job_file_str, setup):
    exception_occurred = False

    cottontail_log_file_path = "logs/cottontail_log.txt"
    cottontail_log_file = None

    cineast_log_file_path = "logs/cineast_log.txt"
    cineast_log_file = None
    try:
        cottontail_log_file = open_log_file(cottontail_log_file_path)
        cottontail_process = __start_cottontail(cottontail_base_path_str, cottontail_log_file)

        cineast_log_file = open_log_file(cineast_log_file_path)
        cineast_process = __start_cineast(cineast_base_path_str, cineast_log_file)
        __extract_from_cineast(cineast_process, cineast_job_file_str, setup=setup)

        cineast_process.communicate()
        cottontail_process.communicate()
    except:
        exception_occurred = True
    finally:
        close_log_file(cottontail_log_file)
        close_log_file(cineast_log_file)

        if exception_occurred:
            print("Finished extraction with errors!")
        else:
            print("Finished extraction successfully")
