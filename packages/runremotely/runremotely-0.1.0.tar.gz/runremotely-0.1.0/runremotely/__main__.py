#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import yaml

DESCRIPTION = """
A script to make it easy to run a command remotely but _in your current directory_
"""

CONFFILE = '.remote'
""" Config format:

- name: [servername]
  host: [URL]
  syncdir: [remote path]
  no-sync: [bool]
  initialized: [bool]
- [...]
"""


def get_argparser():
    parser = argparse.ArgumentParser("remote",
                                     description=DESCRIPTION)

    subparsers = parser.add_subparsers()

    show_cmd = subparsers.add_parser('show', help='Show configured servers')
    show_cmd.add_argument('name',
                         help="Server to show (optional, if not passed, prints all)",
                         nargs='?')
    show_cmd.set_defaults(func=do_show)

    run_cmd = subparsers.add_parser('run', help='Run a command on the remote server')
    run_cmd.add_argument('name', help="Server to run on")
    run_cmd.add_argument('command', nargs=argparse.REMAINDER, help="Remote command to run")
    run_cmd.add_argument('--no-sync', '-n', action='store_true',
                         help="Do not sync before running command")
    run_cmd.set_defaults(func=do_run)

    sync_cmd = subparsers.add_parser('sync', help='Send this directory to the remote one')
    sync_cmd.add_argument('name', help="Server to sync")
    sync_cmd.set_defaults(func=do_sync)

    add_cmd = subparsers.add_parser('add', help='Add a remote server')
    add_cmd.set_defaults(func=do_add)
    add_cmd.add_argument('name', help="A name for this server")
    add_cmd.add_argument('host', help="Hostname")
    add_cmd.add_argument('remote_path', help='Remote directory path', nargs='?')
    add_cmd.add_argument('--no-sync', action='store_true',
                         help="Just run the command _without syncing_ (only makes sense if you're "
                              "running with a network mounted filesystem)")

    return parser


def read_config():
    if not os.path.exists(CONFFILE):
        return None

    with open(CONFFILE, 'r') as infile:
        config = yaml.load(infile)
    return config


def _get_server(config, servername):
    for server in config:
        if servername == server['name']:
            return server
    else:  # this only fires if we don't break (eg, no server with the requested name was found)
        print("ERROR - no remote server named '%s' configured in this directory"
              % servername)
        sys.exit(1)


def do_show(args, config):
    """ Print out the configuration for the current directory (if it exists) and exit.

    Args:
        args (argparse.Namespace): parsed CLI arguments
        config (dict): current config for this directory (or None if it's unconfigured)
    """
    if not config:
        print('No remotes configured.')
        sys.exit(0)

    if args.name:
        to_print = [_get_server(config, args.name)]
    else:
        to_print = config

    print(yaml.dump(to_print))


def do_add(args, config):
    """ Add a new remote to the current configuration

    Args:
        args (argparse.Namespace): parsed CLI arguments
        config (dict): current config for this directory (or None if it's unconfigured)
    """
    if not args.remote_path:
        if not args.no_sync:
            print("ERROR: you must specify a remote path unless syncing is turned off")
            sys.exit(1)
        else:
            remote_path = os.getcwd()
    else:
        remote_path = args.remote_path

    newserver = {'name': args.name,
                 'host': args.host,
                 'nosync': args.no_sync,
                 'syncdir': remote_path,
                 'init': False}

    if config is None:
        config = []
    config.append(newserver)
    with open(CONFFILE, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


def do_run(args, config):
    """ Add a new remote to the current configuration

    Args:
        args (argparse.Namespace): parsed CLI arguments
        config (dict): current config for this directory (or None if it's unconfigured)
    """
    server = _get_server(config, args.name)
    if not (server['nosync'] or args.no_sync):
        sync(server, verbose=False)

    runcmd(args.command, server)



def do_sync(args, config):
    """ Sync the directory to its remote mirror

    Args:
        args (argparse.Namespace): parsed CLI arguments
        config (dict): current config for this directory (or None if it's unconfigured)
    """
    server = _get_server(config, args.name)
    if server['nosync']:
        print('Sync is disabled for this server!')
        sys.exit(1)

    sync(server)


def sync(server, verbose=True):
    remotepath = "%s://%s" % (server['host'], server['syncdir'])
    if verbose: print("Syncing to %s ..." % remotepath)
    subprocess.check_call(['rsync',
                           '-rz' + ('v' if verbose else ''),
                           '.',
                           remotepath])
    if verbose: print("sync done.")


def runcmd(cmd, server):
    subprocess.check_call(["ssh", server['host'],
                           "cd %s && %s" % (server['syncdir'], " ".join(cmd))])


def main():
    args = get_argparser().parse_args()
    config = read_config()
    args.func(args, config)


if __name__ == '__main__':
    main()
