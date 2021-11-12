import pymcprotocol
from time import sleep
from time import time
from pypylon import pylon


ip = "10.18.9.35"
line_values_old = '0'
print(ip)
pymc3e = pymcprotocol.Type3E(plctype="iQ-R")
pymc3e.setaccessopt(commtype="binary")


def getTime(arg):
    return round(arg, 2)


while True:
    cur_time = 0.0
    try:
        # Соединение с контроллером
        pymc3e.connect(ip, 4999)
        print('Connecting...')
        print(f'Connected to {ip}')

        time_prev = time()
        while True:
            line_values = pymc3e.batchread_wordunits(headdevice="D70", readsize=1)  # PLC data

            if line_values_old != line_values:
                time_cur = getTime(time()) - time_prev
                print(f'{getTime(time_cur)} D70= {line_values}')
                '''
                TODO
                Если D70 = код на запрос, то делаем снимок
                Если снимок не получается, то разрываем цикл и пытаемся сконнектиться с камерой 
                '''
            line_values_old = line_values
    except:
        pymc3e.close()
        sleep(1)
        print('Connection problem')