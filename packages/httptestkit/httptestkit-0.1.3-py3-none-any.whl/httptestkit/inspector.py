import time
import socket
import statistics
import sys
from urllib.parse import quote_plus, urlsplit

import dns.resolver

import requests
import tldextract

from httptestkit.plugins import dnskit, headers, ipinfo

class Inspector(object):

    def __init__(self, uri, sleep=None, limit=None, asyncr=False, headers=False, dnsinfo=False, ipinfo=False):
        self.uri = uri
        self.sleep = sleep
        self.limit = limit
        self.asyncr = asyncr
        self.headers = headers
        self.dnsinfo = dnsinfo
        self.ipinfo = ipinfo

    def loop(self):
        num_reqs = 0
        bad_calls = 0
        start = time.time()
        res_time = []

        # Print some bullshit
        print("Testing {0}".format(self.uri))
        print("{0} seconds between requests with a maximum of {1} loops.".format(self.sleep, self.limit))

        if not self.asyncr:
            print("Running in non-asyncronous request mode.\n")

        if self.asyncr:
            print("Running in asyncronous mode.\n")

        while True:
            try:
                if not self.asyncr:
                    num_reqs += 1

                    # fire off the request
                    try:
                        response_timer_init = time.time()
                        req = requests.get(self.uri)
                        response_timer_quit = (time.time() - response_timer_init)
                        res_time.append(response_timer_quit)

                        # return request
                        if req.status_code != requests.codes.ok:
                            bad_calls += 1
                        print(".", end=" ", flush=True)

                        # Back off if requested by the --sleep option
                        if int(self.sleep) > 0:
                            time.sleep(int(self.sleep))

                        # Kill after the number of loops has been exceeded.
                        if int(self.limit) > 0:
                            if int(num_reqs) == int(self.limit):
                                raise ValueError
                    except requests.exceptions.ConnectionError:
                        print("Cannot find a website listening at {0} on port {1}. Aborting.".format(self.uri, "0"))
                        break

                if self.asyncr:
                    try:
                        raise NotImplementedError
                    except NotImplementedError:
                        print("Sorry. Async mode hasn't been implemented yet. Bad dev! No biscuit!")
                        sys.exit(1)

            except (KeyboardInterrupt, ValueError):
                print("\n\nReceived interrupt. Quitting.")
                # Post analysis
                end = (time.time() - start)
                print("Made {0} requests to {1} in {2} seconds with {3} bad status codes\n".format(num_reqs, self.uri, end, bad_calls))

                # Some stats
                print("Statistics:")
                print("===========")
                print("{0:<22}: {1:<18} seconds".format("Average response time", statistics.mean(res_time)))
                print("{0:<22}: {1:<18} seconds".format("Median response time", statistics.median(res_time)))
                print("{0:<22}: {1:<18} seconds".format("Fastest response time", min(res_time)))
                print("{0:<22}: {1:<18} seconds\n".format("Slowest response time", max(res_time)))

                # Show headers if the option has been set
                if self.headers:
                    headers.Headers(self.uri).lookup()

                # Show DNS info if the option has been set
                if self.dnsinfo:
                    dnskit.DNS(self.uri).lookup()

                # Show IP info if the option has been set
                if self.ipinfo:
                    ipinfo.IPInfo(self.uri).lookup()

                print("")
                sys.exit(0)
