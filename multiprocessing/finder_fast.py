import os
import queue
import re
import threading
import time

import server
from finder_helper import charrange, padder, parse_wrong_position


class Handler:
    CHECK_PASSWORD_LENGTH = 1
    TEST_PASSWORD = 2


JOB_WORKER_COUNT = 40

now = time.time()

job_queue = queue.Queue()
answer_queue = queue.Queue()
printer_queue = queue.Queue()


def printer_worker():
    todo = {x: '' for x in range(JOB_WORKER_COUNT)}
    while True:
        data = printer_queue.get()
        if data is False:
            break
        worker_id, testing_now = data
        todo[worker_id] = testing_now
        print("\n" * 100)
        
        for i in range(JOB_WORKER_COUNT):
            tmp = padder(str(i), 2, ' ')
            print(f'worker {tmp}: {todo[i]}')


def worker(worker_id):
    while True:
        data = job_queue.get()
        if data is False:
            printer_queue.put((worker_id, 'dead'))
            break
        job_type, param = data
        test_password = param['test_password']
        printer_queue.put((worker_id, test_password))
        msg = server.validate_password(test_password)
        if job_type == Handler.CHECK_PASSWORD_LENGTH:
            if msg != 'Wrong password length':
                answer_queue.put(len(test_password))
        elif job_type == Handler.TEST_PASSWORD:
            if msg == 'Correct password':
                answer_queue.put(test_password)
            elif msg[:26] == 'Wrong password at position':
                current_position = param['current_position']
                wrong_position = parse_wrong_position(msg)
                if wrong_position > current_position:
                    answer_queue.put(test_password)
        else:
            raise NotImplementedError()


threads = []
for i in range(JOB_WORKER_COUNT):
    thread = threading.Thread(target=worker, args=(i,))
    threads.append(thread)
    thread.start()
thread = threading.Thread(target=printer_worker)
threads.append(thread)
thread.start()


for i in range(40):
    password = 'a' * i
    job_queue.put((Handler.CHECK_PASSWORD_LENGTH, {'test_password': password}))
correct_length = answer_queue.get()


answer = ''
possible_char = [x for x in charrange('a', 'z')] + [x for x in charrange('0', '9')]


for i in range(correct_length):
    for test_char in possible_char:
        test_password = padder(f'{answer}{test_char}', correct_length)
        job_queue.put((Handler.TEST_PASSWORD, {'test_password': test_password, 'current_position': i}))
    answer = answer_queue.get()[:i + 1]


for i in range(JOB_WORKER_COUNT):
    job_queue.put(False)
printer_queue.put(False)

print(f'[password finder]: Found correct password: {answer}\n')
print(f'Finish time: {time.time() - now}')
