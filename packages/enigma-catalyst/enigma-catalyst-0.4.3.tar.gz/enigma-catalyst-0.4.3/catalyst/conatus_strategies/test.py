from redo import retrier

n = 0
for _ in retrier(sleeptime=0, jitter=0):
    if n == 3:
        break

    print('pass')
    raise ValueError('test')
    n += 1
