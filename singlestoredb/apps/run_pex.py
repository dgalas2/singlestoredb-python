import time
import threading
import requests
import subprocess
from ._config import AppConfig

status = False
def ping_port(port, timeout):
    url = f'http://0.0.0.0:{port}/'
    start_time = time.time()

    global status
    while time.time() - start_time < timeout:
        response = requests.get(url, timeout = 2)
        if response.status_code == 200:
            status = True
            return True
        
        time.sleep(10)

    status = False
    return False

def run_pex_app(
	file_path : str,
	time_out : int,
) -> bool:
	
    app_config = AppConfig.from_env()
    port = app_config.listen_port

    print(port)
    process = subprocess.Popen(['python3', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(process.pid)
    ping_thread = threading.Thread(target=ping_port, args=(port,time_out))
    ping_thread.start()

    ping_thread.join()

    return status
