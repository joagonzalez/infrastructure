# .__   __.  _______ ____    __    ____   ______   ______        _______.
# |  \ |  | |   ____|\   \  /  \  /   /  /      | /  __  \      /       |
# |   \|  | |  |__    \   \/    \/   /  |  ,----'|  |  |  |    |   (----`
# |  . `  | |   __|    \            /   |  |     |  |  |  |     \   \    
# |  |\   | |  |____    \    /\    /    |  `----.|  `--'  | .----)   |   
# |__| \__| |_______|    \__/  \__/      \______| \______/  |_______/      

# -------------------------------------------------------------------------
# http api stress script using threads

#!/usr/bin/env python3
import logging
import os
import sys
import time
import threading

# endpoints to stress
cmd = 'curl https://ternium.newtech.com.ar'
cmd2 = 'curl -X POST https://ternium.newtech.com.ar/api/v1/services/request?limit=10'
cmd3 = 'curl -X GET https://ternium.newtech.com.ar/api/v1/services/request?limit=10'

def thread_function(name):
    result = os.system(cmd)
    result2 = os.system(cmd2)
    result3 =  os.system(cmd3)
    time.sleep(0.01)

threads = list()

while True:
    for index in range(20):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)

    time.sleep(0.01)
