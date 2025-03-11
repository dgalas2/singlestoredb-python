import time
import threading
import requests
import subprocess
from ._config import AppConfig
import os
status = False
def ping_port(port, timeout):
    url = f'http://0.0.0.0:{port}/'
    start_time = time.time()

    global status
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout = 2)
            if response.status_code == 200:
                status = True
                break
        except:
            print("Starting Server...")
        
        time.sleep(20)

    return status

def run_pex_app(
	filepath : str,
	timeout : int,
) -> bool:
	
    app_config = AppConfig.from_env()
    port = app_config.listen_port

    print(port)
    print(os.listdir())
    process = subprocess.Popen(['python3', filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(process.pid)
    ping_thread = threading.Thread(target=ping_port, args=(port,timeout))
    ping_thread.start()

    ping_thread.join()
    if not status:
        print("Starting server timed out. Please check if there is an error in your server.")
    else:
        print(f"Server started on port {port}")
    return status
