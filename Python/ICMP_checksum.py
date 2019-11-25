import struct


def accumulate(acc, add):
    '''
    16位累加，超出部分再加到低位上
    :param acc: 累加和
    :param add: 加数
    :return:
    '''
    acc += add
    return (acc & 0xffff) + (acc >> 16)  # 和高于16位的值再加到低16位上


def comp_checksum(msg):
    '''
    计算ICMP报文的校验和
    :param msg: ICMP报文
    :return: 网络字节序的校验和
    '''
    acc = 0
    for i in range(0, len(msg), 2):  # 16bit一组
        group_val = msg[i] + (msg[i + 1] << 8)  # 16bit的值，注意字节顺序
        acc = accumulate(acc, group_val)

    h = ~acc & 0xffff  # host byte order(取反并截取低16位)
    return h >> 8 | (h << 8 & 0xff00)  # network byte order(高8位低8位互换)


if __name__ == '__main__':
    type = 8  # Type: '\x08'(ICMP Echo Request)
    code = 0  # Code: '\x00'
    checksum = 0  # Checksum
    id = 1  # ID: '\x00\x01'
    seq = 251  # Sequence: '\x00\xfb'
    body = b"abcdefghijklmnopqrstuvwabcdefghi"  # Data
    icmp_msg = struct.pack('!BBHHH32s', type, code, checksum, id, seq, body)

    checksum = comp_checksum(icmp_msg)
    assert checksum == 19552  # '\x4c60'
