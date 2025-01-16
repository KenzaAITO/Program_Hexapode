import subprocess
from time import sleep

preview_duration = 0


try : 
    process = subprocess.Popen(["rpicam-hello" , "-t", f"{preview_duration}s", "post-process-file", "1920"])
    sleep(preview_duration)
    

finally:
    process.terminate()
    
    
