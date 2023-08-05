

import urllib
import urllib2
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import re
import os
import time

'''
f = fl3.File(domain='flamingo.exem-oss.org')
f.login('user', 'pw')
f.delete('/user/hive/password/README.md')
f.upload_file('README.md', '/user/hive/password/README.md')

# TO BE
f.chmod('/user/hive/password/README.md', '755')
f.chown('/user/hive/password/README.md', 'hdfs:hdfs')
'''

COOKIE_FILE = os.path.join(str(os.getenv("HOME")), '.fladm_cookie.json')

def build_headers(raw):
    headers = {}

    for line in raw.split('\n'):
        line = line.strip()
        if len(line) > 0:
            t = line.lstrip().split(':')
            headers[t[0]] = t[1].lstrip()

    return headers

def get_filename(filename):
    return filename.split('/')[-1]


class Auth:
    def __init__(self):
        pass

    domain = 'flamingo.exem-oss.org'
    cookie = None
    expired = None

    def exits_cookie(self):
        return os.path.exists(COOKIE_FILE)

    def validate(self):
        if self.exits_cookie():
            self.load_cookie()
            now = time.time()

            if now > self.expired:
                return False

        return bool(re.match('JSESSIONID=[a-zA-Z_0-9]{32}', self.cookie))

    def save_cookie(self):
        f = open(COOKIE_FILE, 'w')
        f.write(json.dumps({
            'domain': self.domain,
            'cookie': self.cookie,
            'expired': time.time() + 600
        }))
        f.close()

    def load_cookie(self):
        f = open(COOKIE_FILE, 'r')
        o = json.loads(f.read())
        self.domain = o['domain']
        self.cookie = o['cookie']
        self.expired = o['expired']

    def login(self, domain, username, password):
        self.domain = domain

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Content-Length': '28',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'flamingo.exem-oss.org',
            'Origin': 'http://flamingo.exem-oss.org',
            'Pragma': 'no-cache',
            'Referer': 'http://flamingo.exem-oss.org/login',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }

        url = 'http://%s/login' % self.domain

        data = urllib.urlencode({
            'username': username,
            'password': password
        })

        s = requests.session()
        s.headers.update(headers)

        s.get(url)
        r = s.post(url, data=data, allow_redirects=False)

        cookie = 'JSESSIONID=%s' % r.cookies.get('JSESSIONID')

        # set cookie to server
        headers['Cookie'] = cookie
        s.headers.update(headers)
        s.get(url)

        self.cookie = cookie
        return cookie

class File:
    auth = None
    domain = None
    cookie = None

    def __init__(self, auth):
        self.auth = auth
        self.domain = auth.domain
        self.cookie = auth.cookie

    def get_headers(self):
        header_raw = '''
            Host: flamingo.exem-oss.org
            Connection: keep-alive
            Content-Length: 19542
            X-CSRF-Token:
            Origin: http://%s
            X-Requested-With: XMLHttpRequest
            User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36
            Content-Type: application/json; charset=UTF-8;
            Accept: */*
            Referer: http://flamingo.exem-oss.org/
            Accept-Encoding: gzip, deflate
            Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
            Cookie: %s
        ''' % (self.domain, self.cookie)

        return build_headers(header_raw)

    def delete(self, filename):
        headers = self.get_headers()
        url = 'http://%s/fs/hdfs/delete.json' % self.domain

        data = json.dumps({
            'currentPath': '/',
            'deleteList': [{
                'fullyQualifiedPath': filename,
                'directory': False
            }]
        })

        r = requests.post(url, data=data, headers=headers)
        return json.loads(r.content)['success']

    def permission(self, filename, group="hdfs", owner="hdfs", permission="644"):
        headers = self.get_headers()
        url = 'http://%s/fs/hdfs/setPermission' % self.domain

        data = json.dumps({
            'currentPath': filename,
            'fileNames': get_filename(filename),
            'fileStatus': 'FILE',
            'files': filename,
            'group': group,
            'owner': owner,
            'permission': permission,
            'recursiveOwner': 0,
            'recursivePermission': 0
        })

        r = requests.post(url, data=data, headers=headers)
        return json.loads(r.content)['success']

    def upload_file(self, filename, dest_filename, overwrite=False):
        if overwrite:
            self.delete(dest_filename)

        headers = self.get_headers()
        url = 'http://%s/fs/hdfs/upload.json' % self.domain

        dstPath = '/'.join(dest_filename.split('/')[0:-1])
        fileName = get_filename(dest_filename)

        form_data = MultipartEncoder(fields={
            'dstPath': dstPath,
            'fileName': (fileName, open(filename, 'rb'))
        })

        headers['Content-Type'] = form_data.content_type

        r = requests.post(url, data=form_data, headers=headers)

        return json.loads(r.content)['success']
