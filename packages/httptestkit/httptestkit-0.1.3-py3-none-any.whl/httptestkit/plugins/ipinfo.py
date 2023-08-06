import dns.resolver
import requests

from httptestkit.plugins import master

class IPInfo(master.Plugin):

    def lookup(self):
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
