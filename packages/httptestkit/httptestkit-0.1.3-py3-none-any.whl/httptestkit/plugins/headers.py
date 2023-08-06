import requests

from httptestkit.plugins import master

class Headers(master.Plugin):

    def lookup(self):
        req = requests.get(self.uri)
        print("Request headers:")
        print("================")
        for k, v in req.headers.items():
            print("{0:<30}{1}".format(k, v))
        print("\n")
