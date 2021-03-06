from scapy.all import *
from datetime import datetime
import os
from MySQL import *
import time

db = MySQL()


def random_mac():
    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def get_ts():
    ts = datetime.utcnow()
    return str(ts.second).zfill(2) + str(ts.microsecond).zfill(6)

while True:
    mac = random_mac()

    os.system("ifconfig h2-eth0 down")
    os.system("ifconfig h2-eth0 hw ether " + mac)
    os.system("ifconfig h2-eth0 up")


    icmp = IP(dst="10.0.0.1") / ICMP()

    t1 = get_ts()
    r1 = sr(icmp, timeout=3)
    t2 = get_ts()
    if not (r1 is None):
        print "timeout 1"
        continue

    t3 = get_ts()
    r2 = sr(icmp, timeout=3)
    t4 = get_ts()
    if not (r2 is None):
        print "timeout 2"
        continue

    sql = "INSERT INTO kw_icmp(`MAC`, `T1`, `T2`, `T3`, `T4`) VALUES('%s', %s, %s, %s, %s)" % (mac, t1, t2, t3, t4)

    db.execute(sql)
    print "%s: %s, %s, %s, %s" % (mac, t1, t2, t3, t4)

    break