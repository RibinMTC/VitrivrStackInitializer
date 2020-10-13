from src.utils.subprocess_communication import *

mlsp_conda_environment = "mlsp_environment"
mlsp_directory = "/home/cribin/Mlsp_Local_Installation/ModifiedMlspProject/src"
ml_predictor_server_start_cmd = "conda activate mlsp_environment " \
                                "&& python mlsp_predictor_server.py " #"/home/cribin/anaconda3/etc/profile.d/conda.sh &&

mlsp_log_file_path = "../logs/mlsp_server_log.txt"

output = run_subprocess(". /home/cribin/anaconda3/etc/profile.d/conda.sh && conda activate mlsp_environment && python mlsp_predictor_server.py", mlsp_directory, True)

# mlsp_server_process = run_subprocess(ml_predictor_server_start_cmd, mlsp_directory)
out, err = output.communicate()
write_bytes_to_log_file(mlsp_log_file_path, out)
write_bytes_to_log_file(mlsp_log_file_path, err)
