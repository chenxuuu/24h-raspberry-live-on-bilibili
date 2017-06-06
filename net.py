#coding:utf8
'''python3 code
author's email: chenyan@feling.net
通过统计ifconfig命令的输出,计算当前网速
'''

import logging
logging.basicConfig(level=logging.INFO,
                format='%(message)s',
                #filename='speed',
                #filemod='w'
                )

import os, sys, time
import re

def get_total_tx_bytes(interface, isCN):
    grep = '发送字节' if isCN else '"TX bytes"'
    r = os.popen('ifconfig '+interface+' | grep '+grep).read()
    total_bytes = re.sub('(.+:)| \(.+','',r)
    return int(total_bytes)

def get_total_rx_bytes(interface, isCN):
    grep = '接收字节' if isCN else '"RX bytes"'
    r = os.popen('ifconfig '+interface+' | grep '+grep).read()
    total_bytes = re.sub(' \(.+','',r)
    total_bytes = re.sub('.+?:','',total_bytes)
    return int(total_bytes)


if __name__=='__main__':
    interface = sys.argv[1]
    get_total_bytes = get_total_tx_bytes if sys.argv[2]=='tx' else get_total_rx_bytes
    isCN = True if sys.argv[3]=='cn' else False
    freq = int(sys.argv[4])
    low_count = 0
    for i in range(1, 30 + 1):
        last = get_total_bytes(interface, isCN)
        time.sleep(freq)
        increase = get_total_bytes(interface, isCN) - last
        logging.info(str(increase/freq/1000))
        speed_now = increase/freq/1000
        if(speed_now < 2):
            low_count = low_count +1
    if(low_count > 28):
        os.system('killall ffmpeg')
        time.sleep(1)
        os.system('killall ffmpeg')
        time.sleep(1)
        os.system('killall ffmpeg')
        logging.info('666')
    else:
        logging.info('ok!')
        
