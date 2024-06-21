import concurrent.futures
import multiprocessing
from time import time

def factorizator(number: int) -> list:
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_normal(*numbers: int) -> list:
    result = []
    for number in numbers:
        result.append(factorizator(number))
    return result

def factorize_multiprocess(*numbers: int) -> list:
    result = []
    with concurrent.futures.ProcessPoolExecutor(multiprocessing.cpu_count()) as executor:
        for numbers in executor.map(factorizator, numbers):
            result.append(numbers)
    return result

if __name__ == '__main__':
    # tests of single core
    start_time1 = time()
    a1, b1, c1, d1  = factorize_normal(128, 255, 99999, 10651060)
    end_time1 = time()
    print(f"Standart calculating: {end_time1 - start_time1}s")

    assert a1 == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b1 == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c1 == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d1 == [
        1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
        380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530,
        10651060
    ]

    # tests of multi-core
    start_time2 = time()
    a2, b2, c2, d2  = factorize_multiprocess(128, 255, 99999, 10651060)
    end_time2 = time()
    print(f"Miltiprosessing calculating: {end_time2 - start_time2}s " \
        f"with {multiprocessing.cpu_count()} cores.")

    assert a2 == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b2 == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c2 == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d2 == [
        1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
        380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530,
        10651060
    ]