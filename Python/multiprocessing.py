import multiprocessing
import time


def func(s: int, e: int, res: int):
    for x in range(s, e):
        res += x
    return res % 1000007


if __name__ == "__main__":
    n = 60000000
    n_cpu = multiprocessing.cpu_count()

    tic = time.time()
    acc = func(0, n, 0)
    toc = time.time()
    print(acc, toc - tic)

    acc = 0
    pool = multiprocessing.Pool(n_cpu)
    results = list()
    tic = time.time()
    for i in range(6):
        s, e = 10000000 * i, 10000000 * (i + 1)
        results.append(pool.apply_async(func, (s, e, 0)))
    for res in results:
        acc += res.get()
        
    pool.close()
    pool.join()
        
    toc = time.time()
    print(acc % 1000007, toc - tic)
