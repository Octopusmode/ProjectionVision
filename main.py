from multiprocessing import Process
from time import sleep, monotonic

import pymcprotocol


controller_addresses = [
    ("10.18.9.10", 4999),
    ("10.18.9.36", 4999),
    ("10.18.9.28", 4999),
    ("10.18.9.29", 4999),
]


def round_time(timestamp):
    return round(timestamp, 2)


def controller_task(controller_host, controller_port):
    old_random_value = None
    controller = pymcprotocol.Type3E(plctype="iQ-R")
    controller.setaccessopt(commtype="binary")

    while True:
        try:
            controller.connect(controller_host, controller_port)
            print(f'Connected to {controller_host}:{controller_port}')

            time_prev = monotonic()
            while True:
                new_random_value = controller.batchread_wordunits(headdevice="D70", readsize=1)

                if old_random_value != new_random_value:
                    time_cur = round_time(monotonic()) - time_prev
                    print(f'{round_time(time_cur)} D70 {controller_host} = {new_random_value}')

                old_random_value = new_random_value

        except Exception as exc:
            controller.close()  # TODO: будет ли ошибка при разрыве соединения?
            print(f'Connection problem: {controller_host} {exc}')
            sleep(0.5)


if __name__ == '__main__':
    controller_threads = []

    for controller_address in controller_addresses:
        print("Connecting to:", controller_address)
        controller_thread = Process(target=controller_task, args=controller_address)
        controller_thread.start()
        controller_threads.append(controller_thread)

    # for controller_thread in controller_threads:
    #     controller_thread.join()