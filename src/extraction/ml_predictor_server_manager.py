import pexpect


def start_ml_predictor_server(main_ml_server_script_path):
    with open("logs/main_ml_predictor_server_log.txt", "w+") as mlsp_log_file:
        ml_server_base_path = get_main_ml_server_base_path(main_ml_server_script_path)
        output = pexpect.spawn("/bin/bash")
        output.logfile = mlsp_log_file.buffer
        output.sendline("cd " + ml_server_base_path)
        output.sendline("venv/bin/python " + main_ml_server_script_path)
        output.expect(["Debug mode: off"], timeout=120)
        print("Main ML- Server has started")
        return output


def get_main_ml_server_base_path(main_ml_server_script_path):
    return main_ml_server_script_path.split("/src")[0]
