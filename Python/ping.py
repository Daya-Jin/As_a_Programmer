import socket, select, struct
import time, sys
from ICMP_checksum import get_checksum


def build_icmpmsg(type, code, checksum, id, seq, data):
    icmp_msg = struct.pack('!BBHHH32s', type, code, checksum, id, seq, data)
    checksum = get_checksum(icmp_msg)
    return struct.pack('!BBHHH32s', type, code, checksum, id, seq, data)


TYPE = 8
CODE = 0
CHECKSUM = 0
ID = 0
SEQ = 1
DATA = b'abcdefghijklmnopqrstuvwabcdefghi'
TIME_OUT = 2
CNT = 4


def pyPing(host):
    cnt_r = 0
    cnt_loss = 0
    ts = list()

    addr_d = socket.gethostbyname(host)    # destination
    print("正在 Ping {} [{}] 具有 32 字节的数据:".format(host, addr_d))

    for i in range(CNT):
        icmp_msg = build_icmpmsg(TYPE, CODE, CHECKSUM, ID, SEQ + i, DATA)
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_RAW,
                             socket.getprotobyname("icmp"))
        tic = time.time()
        sock.sendto(icmp_msg, (addr_d, 80))

        while True:
            start_t = time.time()
            readable = select.select([sock], [], [], TIME_OUT)
            res_t = time.time() - start_t
            if readable[0] == [] or res_t >= TIME_OUT:  # 超时
                cnt_loss += 1
                print("请求超时。")
                break

            toc = time.time()
            t = int((toc - tic) * 1000)
            ts.append(t)

            receive_msg, addr = sock.recvfrom(1024)
            ttl = receive_msg[8]  # TTL: IP首部的第9个字节
            icmp_header = receive_msg[20:28]  # ICMP首部
            type, code, checksum, id, seq = struct.unpack('!BBHHH', icmp_header)

            if type == 0 and seq == SEQ + i:
                cnt_r += 1
                print("来自 {} 的回复: 字节=32 时间={}ms TTL={}".format(addr[0], t, ttl))
                time.sleep(1)

            break

    print('''\n{} 的 Ping 统计信息：
\t数据包：已发送 = {}，已接收 = {} ，丢失 = {} ({:.0%} 丢失)，
'''.format(addr_d,
           CNT, cnt_r, cnt_loss, cnt_loss / CNT), end='')
    if ts:
        print('''往返行程的估计时间(以毫秒为单位)：
\t最短 = {}ms，最长 = {}ms，平均 = {}ms'''.format(min(ts), max(ts), int(sum(ts) / len(ts))))


if __name__ == '__main__':
    host = sys.argv[1]
    pyPing(host)
