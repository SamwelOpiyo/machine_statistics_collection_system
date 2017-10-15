import os
import sys

import psutil

from time import time

from Crypto.Cipher import AES
from Crypto import Random

import json


def encrypt_response(response):
    #  Encryption Key
    key = 'Thirty two encryption byte key!!'
    iv = '16 bit iv key!!!'
    cipher = AES.new(key, AES.MODE_CFB, iv)
    #  Encryption of response
    msg = cipher.encrypt(response)
    return msg


def main():
    #  Creates an empty dictionary to hold the final response of all the system details
    result = {}

    """
    if not hasattr(psutil, "sensors_fans"):
        print "platform not supported for sensors_fans"
    else:
        print psutil.sensors_fans()

    if not hasattr(psutil, "sensors_battery"):
        print "platform not supported for sensors_battery"
    else:
        print psutil.sensors_battery()

    if not hasattr(psutil, "sensors_temperatures"):
        print "platform not supported for sensors_battery"
    else:
        print psutil.sensors_temperatures()

    """

    #  Gets memory details and converts the object into a dictionary
    memory = psutil.virtual_memory().__dict__

    # Gets swap details and converts the object into a dictionary
    swap = psutil.swap_memory().__dict__

    #  Creates an empty dictionary to hold disk partition properties
    disk_partitions = {}
    #  Loops through the disk partition list 
    for each in psutil.disk_partitions():
        """
        Converts the named tuple of disk partion properties into a dictionary 
        and assigns to disk partitions dictionary with key as partition name
        """
        disk_partitions[each[0]] = each._asdict()

    #  Tries getting the root directory disk usage statistics and converts the object to a dictionary
    try:
        disk_usage = psutil.disk_usage('/').__dict__
    #  If not successful, C:// directory disk usage statistics are obtained
    except:
        disk_usage = psutil.disk_usage('C:\\').__dict__

    #  Gets network statistics and converts the object into a dictionary
    network = psutil.net_io_counters().__dict__

    #  Creates an empty dictionary to hold users details
    users = {}
    #  Loops through the users list 
    for each in psutil.users():
        """
        Converts the named tuple of user details into a dictionary 
        and assigns to users dictionary with key as username
        Each value is converted to a string first
        """
        users[each[0]] = dict([(k, str(v)) for k, v in each._asdict().items()])

    CPU = {}
    CPU["cpu_usage"] = float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline())
    CPU["cpu_count"] = psutil.cpu_count()
    CPU["boot_time"] = time() - psutil.boot_time()
    CPU["current_frequency"] = psutil.cpu_freq().current
    CPU["min_frequency"] = psutil.cpu_freq().min
    CPU["max_frequency"] = psutil.cpu_freq().max
    CPU["ctx_switches"] = psutil.cpu_stats().ctx_switches
    CPU["interrupts"] = psutil.cpu_stats().interrupts
    CPU["soft_interrupts"] = psutil.cpu_stats().soft_interrupts
    CPU["syscalls"] = psutil.cpu_stats().syscalls

    """
    try:
        network_connections = {}
        for each in psutil.net_connections(kind="inet"):
            network_connections[each[3][0] + ":" + str(each[3][1])] = dict([(k, v.__dict__) if type(v)==psutil._common.addr else (k, str(v)) for k, v in each._asdict().items()])
    except Exception as error:
        network_connections = None
        print error
    """

    result = {"Platform": sys.platform, "Memory": dict([(k, str(v)) for k, v in memory.items()]), "Swap": dict([(k, str(v)) for k, v in swap.items()]), "DiskPartitions": disk_partitions, "DiskUsage": dict([(k, str(v)) for k, v in disk_usage.items()]), "Network": dict([(k, str(v)) for k, v in network.items()]), "Users": users, "CPU": dict([(k, str(v)) for k, v in CPU.items()])}

    if os.name == 'nt':
        import win32evtlog
        host = 'localhost'
        type_of_log = 'Security'
        hand = win32evtlog.OpenEventLog(host, type_of_log)
        readbck = win32evtlog.EVENTLOG_BACKWARDS_READ
        readsqntl = win32evtlog.EVENTLOG_SEQUENTIAL_READ
        flags = readbck | readsqntl
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events:
            formatedEvents = ''
            for event in events:
                formatedEvents += 'Event Category: ' + str(event.EventCategory)
                formatedEvents += '\nTime Generated: ' + str(event.TimeGenerated)
                formatedEvents += '\nSource Name: ' + event.SourceName
                formatedEvents += '\nEvent ID: ' + str(event.EventID)
                formatedEvents += '\nEvent Type:' + str(event.EventType) + '\n'
            result["logs"] = str(formatedEvents)

    json_result = json.dumps(result)
    #  print result 
    #  print json_result

    msg = encrypt_response(json_result)
    print msg

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
