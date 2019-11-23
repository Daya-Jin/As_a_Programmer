import time


def timer(func):
    def dec():
        tic = time.time()
        func()
        toc = time.time()
        print(toc - tic)

    return dec


if __name__ == '__main__':
    # 调用方式1
    def func():
        print('hello word!')


    func_with_dec = timer(func)
    func_with_dec()


    # 调用方式2
    @timer
    def func():
        print('hello word!')


    func()
