import argparse
import time
import sys

from httptestkit import inspector

def main():
    parser = argparse.ArgumentParser(description='Analyse requests to web sites.')

    parser.add_argument('uri', default='something', help="The URL to query.")

    parser.add_argument('--loop', action="store_true", help="Run in a loop until Ctrl+C is pressed.")
    parser.add_argument('--sleep', default=5, help="Sleep n seconds between interations. Default is 5 seconds. 0 enables spam mode.")
    parser.add_argument('--limit', default=25, help="Limit the number of loops. Default is 25.")
    parser.add_argument('--async', help="Run in asyncronous mode.")
    parser.add_argument('--headers', action="store_true", help="Display the last header received from the request.")
    parser.add_argument('--dnsinfo', action="store_true", help="Do some DNS lookups against the host.")
    parser.add_argument('--ipinfo', action="store_true", help="Do some IPInfo lookups against the host.")

    args = parser.parse_args()

    if args.uri:
        if args.loop:
            # Initiate the basic loop inspector
            inspector.Inspector(args.uri, sleep=args.sleep, limit=args.limit, asyncr=args.async, headers=args.headers, dnsinfo=args.dnsinfo, ipinfo=args.ipinfo).loop()
        else:
            inspector.Inspector(args.uri, sleep=0, limit=1, asyncr=False, headers=args.headers, dnsinfo=args.dnsinfo, ipinfo=args.ipinfo).loop()


if __name__ == "__main__":
    main()
