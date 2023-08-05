import os
import fl3
import sys
import argparse

summary = 'Upload file to HDFS (using Flamingo REST API)'
desc = '''
    %s
    $ flcli upload username:password@domain [local filename] [dest filename]
''' % summary

def print_help():
    print ('*' * 80)
    print (' ' * 25 + 'upload')
    print ('*' * 80)
    print (desc)
    print ('*' * 80)
    print ('*' * 80)

    print ('ex)')
    for usage in get_usage_examples():
        print ('\t' + usage)

def get_usage_examples():
    return [
        '$ flcli upload exem:1234@flamingo-exem.org workflow.xml /flamingo/oozie/test-wf/workflow.xml'
    ]

def main_upload(argv):
    sys.argv = argv

    parser = argparse.ArgumentParser()
    parser.add_argument("-username", help="user name")
    parser.add_argument("-password", help="input password")
    parser.add_argument("-domain", help="domain")
    parser.add_argument("-source", help="Local filename")
    parser.add_argument("-dest", help="HDFS filename")

    parser.add_argument("-own", help="Owner")
    parser.add_argument("-group", help="Group")

    args = parser.parse_args()

    print args

    # if len(argv) >= 4:
    #     connect_info = argv[2]
    #     local_filename = argv[3]
    #     dest_filename = argv[4]
    #
    #     username = connect_info.split(':')[0]
    #     password = connect_info.split(':')[1].split('@')[0]
    #     domain = connect_info.split('@')[1]
    #
    #     # verify local file
    #     if os.path.isfile(local_filename) == False:
    #         print "Not exists file '%s'" % local_filename
    #         exit(1)
    #
    #     f = fl3.File(domain)
    #     f.login(username, password)
    #     r = f.upload_file(local_filename, dest_filename, True)
    #
    #     if r:
    #         print "Upload Success. Local file '%s' -> HDFS file '%s' " % (local_filename, dest_filename)
    #
    # else:
    #   print_help()