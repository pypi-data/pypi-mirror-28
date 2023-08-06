import dns.resolver

from httptestkit.plugins import master


class DNS(master.Plugin):

    def lookup(self):
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
