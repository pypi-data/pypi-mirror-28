# .. an example to test decorator with precision keyword argument ..
"""
Test profiling using command line ``profile`` function (either
``TimeStamper`` or ``LineProfiler``) with precision specified as command
line parameter.
The precision argument specified in the decorator, therefore, is not used.
"""

import time

@profile(precision=4)
def test_1():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    time.sleep(0.6)
    del b

    for i in range(2):
        a = [1] * (10 ** 6)
        b = [2] * (2 * 10 ** 7)
        del b
    return a

@profile(precision=2)
def test_2():
    a = {}
    time.sleep(0.5)
    for i in range(10000):
        a[i] = i + 1
    time.sleep(0.6)
    return

if __name__ == '__main__':
    test_1()
    test_2()
