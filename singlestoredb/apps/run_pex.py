import time
import threading
import requests
import subprocess
from ._config import AppConfig

def ping_port(host, port, timeout):
    url = f'http://{host}:{port}/'
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        response = requests.get(url, timeout = 5)  # 5-second timeout for each request
        if response.status_code == 200:
            return True
        
        time.sleep(1)  # Wait before trying again

    return False

def run_pex_app(
    host,
	file_path : str,
	time_out : int,
) -> bool:
	
	app_config = AppConfig.from_env()
	port = app_config.listen_port
 
	process = subprocess.Popen(['python', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping_thread = threading.Thread(target=ping_port, args=(host, port,time_out))
    ping_thread.start()
    
    ping_thread.join()

    return ping_thread.is_alive()