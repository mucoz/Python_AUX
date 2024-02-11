from time import time
import concurrent.futures
from threading import Thread


def generate_report_1():
    start_time = time()
    x = 0
    for _ in range(10000000):
        x += 1
    end_time = time()
    print(round(end_time-start_time, 2))


def generate_report_2():
    start_time = time()
    x = 0
    for _ in range(10000000):
        x += 1
    end_time = time()
    print(round(end_time-start_time, 2))


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future1 = executor.submit(generate_report_1)
        future2 = executor.submit(generate_report_2)
        concurrent.futures.wait([future1, future2])

    report_1 = Thread(target=generate_report_1)
    report_2 = Thread(target=generate_report_2)
    report_1.start()
    report_2.start()
