from xmlrpc.client import ServerProxy

if __name__ == '__main__':
    server = ServerProxy("http://localhost:4001")  # 初始化代理服务器
    print(server.echo("hello world"))  # 调用函数并传参
