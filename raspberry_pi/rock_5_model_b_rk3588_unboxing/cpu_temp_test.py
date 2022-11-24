import subprocess
import re
import csv
from datetime import datetime
import time
import os
from multiprocessing import Pool
from multiprocessing import cpu_count
import threading
from threading import Event
import argparse

'''
gpu_thermal-virtual-0
Adapter: Virtual device
temp1:        +30.5 C  

littlecore_thermal-virtual-0
Adapter: Virtual device
temp1:        +30.5 C  #6

bigcore0_thermal-virtual-0
Adapter: Virtual device
temp1:        +30.5 C  #10

tcpm_source_psy_4_0022-i2c-4-22
Adapter: rk3x-i2c
in0:           5.00 V  (min =  +5.00 V, max =  +5.00 V)
curr1:         0.00 A  (max =  +0.00 A)

npu_thermal-virtual-0
Adapter: Virtual device
temp1:        +30.5 C  

center_thermal-virtual-0
Adapter: Virtual device
temp1:        +30.5 C  

bigcore1_thermal-virtual-0
Adapter: Virtual device
temp1:        +30.5 C  #27

soc_thermal-virtual-0
Adapter: Virtual device
temp1:        +30.5 C  (crit = +115.0 C)
'''

def sensor(is_csv=False, stop_evt=None):
    if is_csv:
        filename = f'{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
        print(f'Write temperature data to {filename}')

    try:
        while True:
            if stop_evt and stop_evt.is_set():
                break

            sensor_output = subprocess.check_output(['sensors']).decode()
            output_list = sensor_output.split('\n')

            temp_re = re.compile(r'\d+\.?\d*')
            sm_core = temp_re.findall(output_list[6])[1]
            b0_core = temp_re.findall(output_list[10])[1]
            b1_core = temp_re.findall(output_list[27])[1]

            now = datetime.now().strftime("%H:%M:%S")
            print(f'{now}: small core: {sm_core} C, big core 0: {b0_core} C, big core 1: {b1_core} C')

            if is_csv:
                write_csv(filename, [now, sm_core, b0_core, b1_core])

            time.sleep(1)

    except KeyboardInterrupt:
        print('finish')


def write_csv(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if os.stat(filename).st_size == 0:
            writer.writerow(['time', 'sm_core', 'b0_core', 'b1_core'])
        
        writer.writerow(data)


def stress(timeout):
    x = 1
    while True:
        if time.time() > timeout:
            break
        x*x


def run_stress(minute, is_csv):
    stop_evt = Event()
    t = threading.Thread(target=sensor, args=(is_csv, stop_evt,))
    t.start()

    processes = cpu_count()
    print (f'Start stress cpu for {processes} cores in {minute} minutes\n')
    pool = Pool(processes)
    pool.map(stress, [time.time() + 60*minute]*processes)

    stop_evt.set()
    t.join()


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s', '--stress', action="store_true")
    parser.add_argument('-m', '--minute', default=1, type=int)
    parser.add_argument('-c', '--csv', action="store_true")
    args = parser.parse_args()
    if args.stress:
        run_stress(args.minute, args.csv)
    else:
        sensor(args.csv)


if __name__ == '__main__':
    main()