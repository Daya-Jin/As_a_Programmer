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
        group_val = ord(msg[i]) + (ord(msg[i + 1]) << 8)  # 16bit的值，注意字节顺序
        acc = accumulate(acc, group_val)

    h = ~acc & 0xffff  # host byte order(取反并截取低16位)
    return h >> 8 | (h << 8 & 0xff00)  # network byte order(高8位低8位互换)


if __name__=='__main__':
    type = '\x08'  # ICMP Echo Request
    code = '\x00'
    checksum_padding = '\x4c\x60'  # 发送时该字段被置零，接收时抓包查看
    id = '\x00\x01'  # ID，该字段需要抓包查看
    seq = '\x00\xfb'  # Sequence，该字段需要抓包查看
    body = "abcdefghijklmnopqrstuvwabcdefghi"  # 装载数据
    icmp_msg = type + code + checksum_padding + id + seq + body

    checksum = comp_checksum(icmp_msg)
    print('{:x}'.format(checksum))
