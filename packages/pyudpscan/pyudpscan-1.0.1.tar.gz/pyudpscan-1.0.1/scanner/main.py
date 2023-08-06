import argparse

from scanner import Scanner


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--hosts", dest="hosts", type=str,
            nargs="+", default=["127.0.0.1"], help="List of target hosts")
        parser.add_argument("--ports", dest="ports", type=int,
            nargs="+", default=[19], help="List of target ports")
        parser.add_argument("-p", "--proxy", dest="proxies",
            nargs="+", default=None, type=str,
            help="List of proxies which will be taken at random")
        parser.add_argument("-t", "--timeout", dest="timeout",
            type=int, default=1,
            help="How long to wait for reply at UDP request from target host")
        parser.add_argument("-r", "--recheck", dest="recheck", type=int,
            default=0, help="Number of recheck for every port")
        parser.add_argument("-i", "--src-int-address", dest="src_int_address",
            type=str, required=True,
            help=("Address of local source interface to listen on.\n"
                  "Example: 192.168.0.15"))
        args = parser.parse_args()

        s = Scanner(args.proxies, args.hosts, args.ports,
            args.timeout, args.recheck, args.src_int_address)
        for k, v in s.scan().iteritems():
            if k not in ["current_ip", "current_port"]:
                print("{}\t{}".format(k, v))

    except KeyboardInterrupt:
        print('\nThe process was interrupted by the user')
        raise SystemExit


if __name__ == "__main__":
    main()
