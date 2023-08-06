# -*- coding: utf8 -*-
import logging
import multiprocessing
import uuid
from threading import Semaphore
from multiprocessing import Pool
import os
import signal


def process_worker_init(parent_id):
    def sig_int(signal_num, frame):
        os.kill(parent_id, signal.SIGSTOP)

    signal.signal(signal.SIGINT, sig_int)


class MethodWrapper(object):
    def __init__(self, callable_func):
        self.__callable = callable_func

    def __call__(self, *args, **kwargs):
        try:
            self.__callable(*args, **kwargs)
        except KeyboardInterrupt:
            pass


class _MultiProcessControlShim(object):
    @classmethod
    def execute(cls, method, args, callback=None):
        method(*args)
        if callback:
            callback(None)

    def terminate(self):
        pass

    def close(self):
        pass

    def join(self):
        pass


def get_multi_process_control(processes, use_threads=False):
    if processes == 1:
        return _MultiProcessControlShim()

    return _MultiProcessControl(processes, use_threads=use_threads)


class _ShimSemaphore(object):
    def acquire(self):
        pass

    def release(self):
        pass


class _MultiProcessControl(object):
    def __init__(self, processes=-1, max_pending=-1, use_threads=False):
        from multiprocessing.pool import ThreadPool

        processes = multiprocessing.cpu_count() * 2 if processes == -1 else processes
        if use_threads:
            self.__processing_pool = ThreadPool(processes)
        else:
            try:
                self.__processing_pool = Pool(processes, process_worker_init, initargs=(os.getpid(),))
            except AssertionError:
                self.__processing_pool = ThreadPool(processes)

        max_pending_processes = processes * 10 if max_pending == -1 else max_pending
        self.__max_waiting_semaphore = Semaphore(max_pending_processes) if max_pending_processes > 0 else _ShimSemaphore()
        self.__jobs = {}

    def join(self):
        if self.__processing_pool is None:
            return

        self.__processing_pool.join()
        self.__check_pending_jobs()
        logging.debug('%s pool completed', self.__class__)

    def close(self):
        if self.__processing_pool is None:
            return

        logging.debug('%s closing & joining pool', self.__class__)
        self.__processing_pool.close()
        self.join()

    def create_callback(self, token, callback):
        def do_callback(param):
            self.__max_waiting_semaphore.release()
            if callback is not None:
                callback(param)

        return do_callback

    def __check_pending_jobs(self):
        for token, async_result in self.__jobs.items():
            if async_result is None:
                continue

            if not async_result.ready():
                continue

            async_result.get()
            self.__jobs[token] = None

        self.__jobs = {token: async_result for token, async_result in self.__jobs.items() if async_result is not None}

    def execute(self, method, args, callback=None):
        self.__max_waiting_semaphore.acquire()

        self.__check_pending_jobs()

        token = uuid.uuid4()
        job_async_result = self.__processing_pool.apply_async(
            MethodWrapper(method),
            args=args,
            callback=self.create_callback(token, callback))

        self.__jobs[token] = job_async_result

        return job_async_result

    def terminate(self):
        self.__processing_pool.terminate()
