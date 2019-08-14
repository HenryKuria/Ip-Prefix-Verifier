#!/usr/bin/python3

import os
import sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from subprocess import Popen, PIPE


def check_ip(ip_addr, test_origin):
    
    # Query on Afrinic
    
    # grep origin
    database = 'AfriNIC'
    p = Popen(["whois", "-h" "whois.afrinic.net", '{}'.format(ip_addr)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    asn = Popen(["grep", "origin"], stdin=p.stdout, stdout=PIPE, stderr=PIPE) 

    (origin, err) = asn.communicate()

    if origin == b'':
        origin = 'Ip has no route object'
    else:
        origin = origin[16:].decode("utf-8").rstrip()

    return "tested ip: {} | tested origin: {} | found: {} | match: {} | database {}".format(ip_addr, test_origin, origin, origin == test_origin, database)


df = pd.read_excel('~/Downloads/Documents/PrefixVerificationM.xlsx', index_col=[0, 1])
for index, row in df.iterrows():
    print(check_ip('{}'.format(index[0]), '{}'.format(index[1])))
