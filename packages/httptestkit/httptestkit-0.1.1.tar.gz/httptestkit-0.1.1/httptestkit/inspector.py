import time
import socket
import statistics
import sys
from urllib.parse import quote_plus, urlsplit

import dns.resolver

import requests
import tldextract

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
                    self.get_headers()

                # Show DNS info if the option has been set
                if self.dnsinfo:
                    self.get_dnsinfo()

                # Show IP info if the option has been set
                if self.ipinfo:
                    self.get_ipinfo()

                print("")
                sys.exit(0)

    def get_headers(self):
        req = requests.get(self.uri)
        print("Request headers:")
        print("================")
        for k, v in req.headers.items():
            print("{0:<30}{1}".format(k, v))
        print("\n")

    def _split_hostname(self):
        parsed = urlsplit(self.uri)
        return parsed.netloc

    def _split_domain(self):
        ext = tldextract.extract(self.uri)
        domain = "{0}.{1}".format(ext.domain, ext.suffix)
        return domain

    def get_dnsinfo(self):
        # For NS and SOA queries
        # ext = tldextract.extract(self.uri)
        # domain = "{0}.{1}".format(ext.domain, ext.suffix)
        domain = self._split_domain()

        # For "other"
        # parsed = urlsplit(self.uri)
        # host = parsed.netloc
        host = self._split_hostname()

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['8.8.8.8']
        ns = dns.resolver.query(domain, 'NS')
        ar = dns.resolver.query(host, 'A')

        line = "Nameservers for {0} are:".format(domain)
        print(line)
        print("=" * len(line))
        for rr in ns:
            print(rr.target)

        try:
            cn = dns.resolver.query(host, 'CNAME')
            rdt = dns.rdatatype.to_text(cn.rdtype)
            print("\n{0} is a {1} record.".format(host, rdt))
        except dns.resolver.NoAnswer:
            pass

        line = "\nThe host {0} resolves to:".format(host)
        print(line)
        print("=" * len(line))
        for rr in ar:
            rdt = dns.rdatatype.to_text(ar.rdtype)
            req = '.'.join(reversed(str(rr).split("."))) + ".in-addr.arpa"
            ptr = dns.resolver.query(req, 'PTR')
            for ra in ptr:
                rev = ra
            print("[{0}] {1} ({2})".format(rdt, rr, rev))

    def get_ipinfo(self):
        # Resolve A records
        host = self._split_hostname()
        rec = dns.resolver.query(host, 'A')

        line = "\nIP info for {0}:".format(host)
        print(line)
        print("=" * len(line))
        headers = {'Accept': 'application/json'}
        for rr in rec:
            req = requests.get("https://ipinfo.io/{0}".format(rr), headers=headers)
            res = req.json()
            for k, v in res.items():
                if len(k) == 2:
                    fmt = str(k).upper()
                else:
                    fmt = str(k).capitalize()

                print("{0:<20}: {1}".format(fmt, v))
            (lat, lon) = res['loc'].split(",")
            maps_url = "https://www.google.com/maps/search/?api=1&query={0},{1}".format(lat, lon)
            print("{0:<20}: {1}".format("Google Maps", maps_url))

    def get_security(self):
        pass
