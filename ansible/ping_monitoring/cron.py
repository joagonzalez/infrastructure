#!/usr/bin/env python3
import os
import time

cmd = 'ansible-playbook playbook.yaml -i hosts'

while True:
    os.system(cmd)
    print('esperamos 10 segundos para otro muestreo...')
    time.sleep(10)
