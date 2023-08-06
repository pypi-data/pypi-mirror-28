#!/usr/bin/env python

import sys
from . import awsapi


def check_args_or_exit(args):
    # type: (list[str]) -> None
    valid = False
    if len(args) == 1 and args[0] in ("update-ssh", "rescan"):
        valid = True
    elif len(args) == 2 and args[0] in ("start", "stop", "terminate", "show", "describe", "info") and args[1]:
        valid = True
    elif len(args) == 5 and args[0] in ("create", "new") and args[1] and args[2] and args[3] and args[4]:
        # awsmpi create <name> <vm-count> <vm-type> <shared-volume-size>
        valid = True
    if not valid:
        print("""awsmpi - manage your MPI cluster on AWS.
Commands:
    awsmpi create <name> <vm-count> <vm-type> <shared-volume-count>
    awsmpi start <name>
    awsmpi stop <name>
    awsmpi show|describe <name>
    awsmpi terminate <name>

For detailed documentation, please refer to https://github.com/WenbinHou/awsmpi
""")
        exit(1)


def main(args):
    # type: (list[str]) -> None

    # Check arguments, or print help information and exit
    check_args_or_exit(args)

    client = awsapi.Client(args)
    if args[0] in ("create", "new"):
        # awsmpi create <name> <vm_count> <vm_type> <shared_volume>
        client.create()
    elif args[0] in ("terminate", "destroy"):
        # awsmpi terminate <name>
        client.terminate()
    elif args[0] in ("show", "describe", "info"):
        # awsmpi terminate <name>
        client.describe()
    elif args[0] == "start":
        # awsmpi start <name>
        client.start()
    elif args[0] == "stop":
        # awsmpi stop <name>
        client.stop()


def entrypoint():
    """
    This is reserved for PyPI package entrypoint.
    """
    main(sys.argv[1:])
    pass


if __name__ == '__main__':
    entrypoint()
