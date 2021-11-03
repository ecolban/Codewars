from random import randrange


def sender(input_stream, window_size):
    tx_window = [None] * window_size
    i, start, num_items_in_tx_window = 0, 0, 0

    def send():
        nonlocal num_items_in_tx_window
        j, none_count = 0, 0
        choice = randrange(num_items_in_tx_window)
        for j in range(start, start + choice + 1):
            while tx_window[(j + none_count) % window_size] is None:
                none_count += 1
        choice = (start + choice + none_count) % window_size
        yield choice, tx_window[choice]
        tx_window[choice] = None
        num_items_in_tx_window -= 1

    try:
        while True:
            while tx_window[start] is None:
                tx_window[start] = next(input_stream)
                num_items_in_tx_window += 1
                start = (start + 1) % window_size
            while tx_window[start] is not None:
                yield from send()
    except StopIteration:
        for _ in range(num_items_in_tx_window):
            yield from send()


def receiver(in_stream, window_size):
    buffer = [None] * window_size
    start = 0
    for i, v in in_stream:
        buffer[i] = v
        if i == start:
            while buffer[start] is not None:
                yield buffer[start]
                buffer[start] = None
                start = (start + 1) % window_size


def test_send_receive():
    window_size = 5
    stream = (str(i) for i in range(100))
    a = list(sender(stream, window_size))
    print(', '.join(v for _, v in a))
    b = receiver(a, window_size)
    print(', '.join(b))


if __name__ == '__main__':
    test_send_receive()
