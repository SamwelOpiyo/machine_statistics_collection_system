import paramiko

import codecs
import xmltodict

import os
import sys

from Crypto.Cipher import AES

import json

from datetime import datetime

import sqlite3


def decrypt_response(response):
    key = 'Thirty two encryption byte key!!'
    iv = '16 bit iv key!!!'
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = cipher.decrypt(response[:-1])
    #  print msg
    print "Response Decrypted Successfully."
    return msg


def connect(ip, port, username, password, email):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, username, password)
        print "SSH connection Successful."
        sftp_client = ssh.open_sftp()

        stdin, stdout, stderr = ssh.exec_command('echo "test"')
        stdin.close()
        response = str(stdout.read())
        returnedQuotation = response.find('"')
        if returnedQuotation == -1:
            windows = False
        else:
            windows = True

        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not windows:
            path = "/tmp/"
            command = 'sudo python /tmp/Client_Script.py'

        else:
            path = "C:\\Windows\\Temp\\"
            command = "python C:\\Windows\\Temp\\Client_Script.py"
 
        if not os.path.exists(path):
            os.makedirs(path)
        sftp_client.put(parent_directory + '/Source/Client_Script.py', path + 'Client_Script.py')
        print "File Transfer Successful."

        stdin, stdout, stderr = ssh.exec_command(command)
        if not windows:
            stdin.write(password + '\n')
            stdin.flush()
            stdin.close()
        #  for line in stdout.readlines():
            #  print line.strip()
        response_ssh = stdout.read()
        #  print response

        msg = decrypt_response(response_ssh)
 
        msg = json.loads(msg)
        print "Json response converted into a Python Dictionary Successfully."
       
        sftp_client.close()
        ssh.close()
        return msg

    except paramiko.ssh_exception.AuthenticationException:
        print "Authentication has failed!"
        quit()
 
    except paramiko.ssh_exception.BadHostKeyException:
        print "Server hostkey could not be verified!"
        quit()
   
    except paramiko.ssh_exception.SSHException:
        print "Error connecting or establishing SSH Session!"
        quit()
 
    except paramiko.ssh_exception.socket.error:
        print "Socket error occurred while connecting!"
        quit()
  
    except IOError:
        print "IOError while trying to read file!"
        quit()

    except:
        print "Unknown exception: {0}!".format(str(sys.exc_info()[0]))
        quit()


def main():
    try:
        xml = codecs.open("config.xml", encoding="UTF-8")
        u = xml.read()
        print "Config variables read Successfully."
        xml.close()
    except:
        print "Error Opening File"
        quit()

    clients = xmltodict.parse(u)

    for client in clients:
        ip = str(clients[client]["client"]["@ip"])
        port = int(clients[client]["client"]["@port"])
        username = str(clients[client]["client"]["@username"])
        password = str(clients[client]["client"]["@password"])
        email = str(clients[client]["client"]["@mail"])
        msg = connect(ip, port, username, password, email)
        time = str(datetime.now())

        #  connects to a sqlite database(file), greenshoe.db, if it exists or creates it
        conn = sqlite3.connect('NetworkData.db')
        print "Opened database successfully."

        if len(conn.execute("select id from systemdetails where ip_address = '" + ip + "';").fetchall()) == 0:
            conn.execute("INSERT INTO systemdetails (ip_address, platform, date_entry) \
                          VALUES ('" + ip + "', '" + msg["Platform"] + "', '" + time + "');")

        for each in msg["Users"]:
            conn.execute(("INSERT INTO systemusers (name, terminal, host, started, date_entry, ip_id) \
                          VALUES ('" + msg["Users"][each]["name"] + "', '" + msg["Users"][each]["terminal"] + "', '" + msg["Users"][each]["host"] + "', '" + msg["Users"][each]["started"] + "', '" + time + "', (select id from systemdetails where ip_address = '" + ip + "'));"))

        for each in msg["DiskPartitions"]:
            conn.execute("INSERT INTO diskpartitions (fstype, device, mountpoint, opts, date_entry, ip_id) \
                          VALUES ('" + msg["DiskPartitions"][each]["fstype"] + "', '" + msg["DiskPartitions"][each]["device"] + "', '" + msg["DiskPartitions"][each]["mountpoint"] + "', '" + msg["DiskPartitions"][each]["opts"] + "', '" + time + "', (select id from systemdetails where ip_address = '" + ip + "'));")

        conn.execute("INSERT INTO swap (used, percent, free, sin, sout, total, date_entry, ip_id) \
                      VALUES ('" + msg["Swap"]["used"] + "', '" + msg["Swap"]["percent"] + "', '" + msg["Swap"]["free"] + "', '" + msg["Swap"]["sin"] + "', '" + msg["Swap"]["sout"] + "', '" + msg["Swap"]["total"] + "', '" + time + "', (select id from systemdetails where ip_address = '" + ip + "'));")

        conn.execute("INSERT INTO memory (available, used, cached, percent, free, inactive, active, shared, total, buffers, date_entry, ip_id) \
                      VALUES ('" + msg["Memory"]["available"] + "', '" + msg["Memory"]["used"] + "', '" + msg["Memory"]["cached"] + "', '" + msg["Memory"]["percent"] + "', '" + msg["Memory"]["free"] + "', '" + msg["Memory"]["inactive"] + "', '" + msg["Memory"]["active"] + "', '" + msg["Memory"]["shared"] + "', '" + msg["Memory"]["total"] + "', '" + msg["Memory"]["buffers"] + "', '" + time + "', (select id from systemdetails where ip_address = '" + ip + "'));")

        conn.execute("INSERT INTO diskusage (used, percent, free, total, date_entry, ip_id) \
                      VALUES ('" + msg["DiskUsage"]["used"] + "', '" + msg["DiskUsage"]["percent"] + "', '" + msg["DiskUsage"]["free"] + "', '" + msg["DiskUsage"]["total"] + "', '" + time + "', (select id from systemdetails where ip_address = '" + ip + "'));")

        if "logs" in msg.iterkeys():
            conn.execute("INSERT INTO cpu (current_frequency, cpu_usage, soft_interrupts, min_frequency, cpu_count, max_frequency, boot_time, syscalls, interrupts, ctx_switches, logs, date_entry, ip_id) \
                          VALUES ('" + msg["CPU"]["current_frequency"] + "', '" + msg["CPU"]["cpu_usage"] + "', '" + msg["CPU"]["soft_interrupts"] + "', '" + msg["CPU"]["min_frequency"] + "', '" + msg["CPU"]["cpu_count"] + "', '" + msg["CPU"]["max_frequency"] + "', '" + msg["CPU"]["boot_time"] + "', '" + msg["CPU"]["syscalls"] + "', '" + msg["CPU"]["interrupts"] + "', '" + msg["CPU"]["ctx_switches"] + "', '" + msg["logs"] + "', '" + time + "', (select id from systemdetails where ip_address = '" + ip + "'));")
        else:
            conn.execute("INSERT INTO cpu (current_frequency, cpu_usage, soft_interrupts, min_frequency, cpu_count, max_frequency, boot_time, syscalls, interrupts, ctx_switches, date_entry, ip_id) \
                          VALUES ('" + msg["CPU"]["current_frequency"] + "', '" + msg["CPU"]["cpu_usage"] + "', '" + msg["CPU"]["soft_interrupts"] + "', '" + msg["CPU"]["min_frequency"] + "', '" + msg["CPU"]["cpu_count"] + "', '" + msg["CPU"]["max_frequency"] + "', '" + msg["CPU"]["boot_time"] + "', '" + msg["CPU"]["syscalls"] + "', '" + msg["CPU"]["interrupts"] + "', '" + msg["CPU"]["ctx_switches"] + "', '" + time + "', (select id from systemdetails where ip_address = '" + ip + "'));")

        conn.execute("INSERT INTO network (packets_sent, bytes_recv, packets_recv, dropin, dropout, bytes_sent, errout, errin, date_entry, ip_id) \
                      VALUES ('" + msg["Network"]["packets_sent"] + "', '" + msg["Network"]["bytes_recv"] + "', '" + msg["Network"]["packets_recv"] + "', '" + msg["Network"]["dropin"] + "', '" + msg["Network"]["dropout"] + "', '" + msg["Network"]["bytes_sent"] + "', '" + msg["Network"]["errout"] + "', '" + msg["Network"]["errin"] + "', '" + time + "', (select id from systemdetails where ip_address = '" + ip + "'));")

        #  Make the changes requested
        conn.commit()
        print "Records created successfully."
        #  close the connection to the database after creating the table
        conn.close()

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
