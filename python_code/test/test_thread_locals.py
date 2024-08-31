import asyncio
import threading
import time
from collections import defaultdict
from functools import wraps, partial

import pytest

THREAD_LOCALS = threading.local()


def get_session():
    if not hasattr(THREAD_LOCALS, 'session'):
        session = object()
        THREAD_LOCALS.session = session
    return THREAD_LOCALS.session


def async_function(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(f, *args, **kwargs))

    return wrapper


@pytest.mark.asyncio
async def test_get_thread_session_mapping_async():
    @async_function
    def h():
        time.sleep(0.1)
        return threading.current_thread().name, id(get_session())

    res = await asyncio.gather(*(h() for _ in range(100)))
    thread_sessions = defaultdict(set)
    for thread_name, session_id in res:
        thread_sessions[thread_name].add(session_id)

    # each thread has a single local session
    assert all(len(session) == 1 for session in thread_sessions.values())
    # the sessions are distinct
    assert len(thread_sessions.keys()) == len({session_id for _, session_id in res})


class InsufficientFundsException(Exception):
    pass



class Account:

    def __init__(self):
        self._balance = 0
        self._lock = threading.Lock()

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        self._lock.acquire()
        if amount <= self._balance:
            time.sleep(1e-9)
            self._balance -= amount
        self._lock.release()

    @property
    def balance(self):
        return self._balance


def worker(account: Account, amount: int, barrier: threading.Barrier):
    barrier.wait()
    account.withdraw(amount)


def test_withdrawals():
    num_threads = 101
    barrier = threading.Barrier(num_threads)
    account = Account()
    account.deposit(100)
    ts = [threading.Thread(target=worker, args=(account, 1, barrier)) for _ in range(num_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert account.balance >= 0
