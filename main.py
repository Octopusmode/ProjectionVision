from multiprocessing import Process
from time import sleep, monotonic
from PIL import Image
from pypylon import pylon

import pymcprotocol

controller_addresses = [
    ("192.168.0.159", 4199)  # 4999 for iQ-R
]


def round_time(timestamp) :
    return round(timestamp, 9)


def controller_task(controller_host, controller_port) :
    request_code_old = None
    controller = pymcprotocol.Type3E()  # (plctype="iQ-R")
    # controller.setaccessopt(commtype="binary")

    while True :
        try:
            camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        except Exception as exc:
            print(f'Camera problem: {exc}')
            pass

        try :
            controller.connect(controller_host, controller_port)
            print(f'Connected to {controller_host}:{controller_port}')

            while True :
                time_prev = monotonic()
                request_code_new = controller.batchread_wordunits(headdevice="D5000", readsize=1)

                if request_code_old != request_code_new :
                    time_cur = round_time(monotonic()) - time_prev
                    print(f'{round_time(time_cur)} D5000 {controller_host} = {request_code_new}')
                    controller.randomwrite_bitunits(bit_devices=["B10"], values=[1])

                request_code_old = request_code_new

        except Exception as exc :
            controller.close()  # TODO: будет ли ошибка при разрыве соединения?
            print(f'Connection problem: {controller_host}:{controller_port} {exc}')
            sleep(0.5)


if __name__ == '__main__' :
    controller_threads = []

    for controller_address in controller_addresses :
        print("Connecting to:", controller_address)
        controller_thread = Process(target=controller_task, args=controller_address)
        controller_thread.start()
        controller_threads.append(controller_thread)

    # for controller_thread in controller_threads:
    #     controller_thread.join()
