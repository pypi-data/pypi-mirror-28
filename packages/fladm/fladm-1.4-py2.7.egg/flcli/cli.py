#!/usr/bin/python
import os
import sys
import json
import upload
import argparse
import fl3

def print_help():
    print ('*' * 80)
    print (' ' * 24 + 'Flamingo CLI')
    print ('*' * 80)
    print (' Available commands')
    print ('-' * 80)
    print ('  upload\t\t\t%s' % upload.summary)
    print ('*' * 80)

    print ('examples)')
    for usage in upload.get_usage_examples():
        print ('\t' + usage)

def login(args):
    print 'login... user=%s pw=%s domain=%s' % (args.user, args.pw, args.domain)
    auth = fl3.Auth()
    auth.login(args.domain, args.user, args.pw)
    auth.save_cookie()

    if auth.validate():
        print 'Success'
    else:
        exit(1)

def upload(args):
    print 'uploading... source=%s dest=%s permission=%s own=%s group=%s' % (args.source, args.dest, args.permission, args.own, args.group)
    auth = fl3.Auth()
    auth.load_cookie()

    file = fl3.File(auth)
    r = file.upload_file(args.source, args.dest, True)

    if args.own or args.group or args.permission:
        file.permission(args.dest, owner=args.own, group=args.group, permission=args.permission)

    if r:
        print 'Success'
    else:
        exit(1)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # login
    parser_hdfs = subparsers.add_parser('login')
    parser_hdfs.add_argument('-user', help="Flamingo WEB username", required=True)
    parser_hdfs.add_argument('-pw', help="Flamingo WEB password", required=True)
    parser_hdfs.add_argument('-domain', help="Flamingo WEB domain", required=True)
    parser_hdfs.set_defaults(func=login)

    # upload
    parser_hdfs = subparsers.add_parser('upload')
    parser_hdfs.add_argument('-source', help="local filename (source)", required=True)
    parser_hdfs.add_argument('-dest', help="HDFS filename (destination)", required=True)
    parser_hdfs.add_argument('-permission', help="Permission (644|755)", default="644")
    parser_hdfs.add_argument('-own', help="Owner username 'hdfs", default="hdfs")
    parser_hdfs.add_argument('-group', help="Group name 'hdfs", default="hdfs")
    parser_hdfs.set_defaults(func=upload)

    parser.parse_args()
    args = parser.parse_args(sys.argv[1:])
    args.func(args)

if __name__ == '__main__':
    main()