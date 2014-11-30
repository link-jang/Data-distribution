

import subprocess,time

def  command(cmd, timeout=120):  

    p = subprocess.Popen(cmd, stdout = subprocess.PIPE)  
    t_beginning = time.time()  
    seconds_passed = 0  
    while True:  
        if p.poll() is not None:  
            break  
        seconds_passed = time.time() - t_beginning  
        if timeout and seconds_passed > timeout:  
            p.terminate()  
            return (1, 'timeout: ' + str(seconds_passed))
        time.sleep(0.1)  
    return (0, p.stdout.read()) 