import pymcprotocol
from time import sleep
from time import time
from pypylon import pylon
# import cv2

ip = "192.168.0.159"
line_values_old = '0'
print(ip)
pymc3e = pymcprotocol.Type3E()


def getTime(arg):
    return round(arg, 2)


while True:
    cur_time = 0.0
    try:
        # Соединение с контроллером
        pymc3e.connect(ip, 4199)
        print('Connecting...')
        print(f'Connected to {ip}')

        # Соединение с камерой
        # camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        # camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        # converter = pylon.ImageFormatConverter()
        # converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        # converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        time_prev = time()
        while True:
            # grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)  # Cam data

            line_values = pymc3e.batchread_wordunits(headdevice="D5000", readsize=1)  # PLC data

            if line_values_old != line_values:
                time_cur = getTime(time()) - time_prev
                print(f'{getTime(time_cur)} D5000 = {line_values}')
                '''
                TODO
                Если D5000 = код на запрос, то делаем снимок
                Если снимок не получается, то разрываем цикл и пытаемся сконнектиться с камерой 
                '''
            line_values_old = line_values
    except:
        pymc3e.close()
        sleep(1)
        print('Connection problem')