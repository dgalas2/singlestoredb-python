import time
import threading
import requests
import subprocess
from ._config import AppConfig

def run_pex_app(
	file_path : str,
	time_out : int,
):
	
    app_config = AppConfig.from_env()
    port = app_config.listen_port

    print(port)
    process = subprocess.Popen(['python3', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return process.pid
