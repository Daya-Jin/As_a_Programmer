from xmlrpc.server import SimpleXMLRPCServer


def func(s):
    '''
    服务器端的函数
    '''
    return s


if __name__ == '__main__':
    # 初始化一个服务器对象
    server = SimpleXMLRPCServer(('localhost', 4001))
    # 注册函数，字串参数指明远程调用的方法
    server.register_function(func, "echo")  # 远程调用使用echo方法
    print("Listening for Client")
    server.serve_forever()  # 保持服务
