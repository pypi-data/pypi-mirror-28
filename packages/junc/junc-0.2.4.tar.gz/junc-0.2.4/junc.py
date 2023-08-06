"""
Usage:
    junc list [--json]
    junc connect <name>
    junc add [(<name> <username> <ip>)] [<location>]
    junc remove <name>
    junc backup [<file>]
    junc restore [<file>]

Options:
    -h --help     Show this screen.
    --version     Show version.
    --json        Output server list as JSON instead of a (readable) table

Arguments:
    name          Human-readable name of a server
    username      Username you wish to login with
    ip            The IP of the server
    location      (Optional) Where the server is located (useful for headless machines ie. raspberry pi)
    file          A backup is created at (or restored from) this location (default: ~/.junc.json.bak)

Notes:
    Data is stored in ~/.junc.json
    Default backup location is ~/.junc.json.bak
"""

import os
import sys

from docopt import docopt
from contextlib import suppress
import json
from version import VERSION

from storage import Storage

def new_server(args):
    attr_list = ['<ip>', '<username>', '<name>', '<location>']
    new_server = {}
    for attr in attr_list:
        if attr in args.keys():
            # cut off the < and >
            pretty_attr = attr[1:-1]
            new_server[pretty_attr] = args[attr]
    return new_server

def cli(args):
    storage = Storage()
    try:
        server_list = storage.get_servers()
    except PermissionError:
        print('Error: Permission denied. Try again with sudo or change permissions on ' + storage.file_path + ' (Recommended)')
        return False

    if args['add']:
        while not args['<name>'] or not args['<ip>'] or not args['<username>']:
            args['<name>'] = input('Name: ')
            args['<username>'] = input('Username: ')
            args['<ip>'] = input('IP: ')
            args['<location>'] = input('Location: ')
            if not args['<name>'] or not args['<ip>'] or not args['<username>']:
                print('Please fill out all the fields')
                print('\n')
        server_list.append(new_server(args))
        storage.write(server_list)
        args['list'] = True

    if args['list']:
        server_table = storage.get_server_table()
        if args['--json']:
            print(json.dumps(server_list, indent=2))
            return server_list
        print(server_table)
        return server_table

    if args['connect']:
        connection = ''
        for server in server_list:
            if server['name'] == args['<name>']:
                connection = server['username'] + '@' + server['ip']
        if not connection:
            print("Couldn't find that server...")
            return False
        print('Connecting...')
        os.system('ssh ' + connection)
        return True

    if args['remove']:
        for i in range(len(server_list)):
            if server_list[i]['name'] == args['<name>']:
                print(server_list[i]['name'] + ' removed')
                del server_list[i]
                storage.write(server_list)
                return server_list
            if i == len(server_list) - 1:
                print("Couldn't find that server...")
                return False

    if args['backup']:
        storage.backup(args['<file>'])
        return True

    if args['restore']:
        print('This will overwrite your current', storage.file_path)
        choice = input('Are you sure? (y/n)')
        if choice in ['y', 'Y', 'yes']:
            storage.restore(args['<file>'])
            return True
        else:
            print('Canceled')
            return False
def main():
    arguments = docopt(__doc__, version='Junc v' + VERSION)
    with suppress(KeyboardInterrupt):
        if not cli(arguments):
            sys.exit(1)
    print('\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
