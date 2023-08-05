#!/usr/bin/python
import sys
import paramiko
import time
import urllib2

def test1():
    host = 'localhost'
    user = 'exem'
    pw = 'exem'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    stdin, stdout, stderr = ssh.exec_command('whoami')
    print(stdout.read())

def test2():
    host = 'localhost'
    user = 'exem'
    pw = 'exem'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    ch = ssh.invoke_shell()
    ch.recv(9999)
    ch.send('whoami\n')

    while not ch.recv_ready():
        time.sleep(3)

    out = ch.recv(9999)
    print (out)

def test3():
    while True:
        print ('1')
        time.sleep(1)

def test_urllib2():
    headers = {
        ':authority': 'www.googleapis.com',
        ':method': 'GET',
        ':path': '/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=ko&prettyPrint=false&source=gcsc&gss=.kr&sig=ebaa7a3b8b3fa3d882a727859972d6ad&cx=partner-pub-9536564912915906:8564639793&q=%EC%A2%8B%EC%95%84%20%EB%AF%BC%EC%84%9C&cse_tok=AOdTmaASPu2Ljo5RyXb50XNzOZrYSssKNQ:1512898078620&sort=&googlehost=www.google.com&oq=%EC%A2%8B%EC%95%84%20%EB%AF%BC%EC%84%9C&gs_l=partner.12...0.0.1.13045.0.0.0.0.0.0.0.0..0.0.gsnos%2Cn%3D13...0.0jj1..1ac..25.partner..0.0.0.&callback=google.search.Search.apiary3001&nocache=1512898079182',
        ':scheme': 'https',
        'accept': '*/*',
        # 'accept-encoding:gzip, deflate, br
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'http://www.lyrics.co.kr/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'x-chrome-uma-enabled': '1',
        'x-client-data': 'CIu2yQEIpbbJAQjEtskBCPqcygEIqZ3KAQioo8oB'
    }

    req = urllib2.Request('http://flamingo.exem-oss.org/config/js.json')

    # for h in headers:
    #     req.add_header(h, headers[h])

    html = urllib2.urlopen(req).read()
    print (html)

import socket
def test_port_scan():
    remoteServerIP = 'flamingo.exem-oss.org'
    ports = [80, 8080, 9000, 443, 8443]

    try:
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print "Port {}: 	 Open".format(port)
            else:
                print "Port {}: 	 Closed".format(port)

            sock.close()

    except KeyboardInterrupt:
        print "You pressed Ctrl+C"

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'

    except socket.error:
        print "Couldn't connect to server"


def signal_handler(signal, frame):
    print ('yyy')
    sys.exit(0)

def main(argv):
    test_port_scan()

if __name__ == '__main__':
    main(sys.argv)