from urllib.parse import quote_plus, urlsplit

import tldextract

class Plugin(object):

    def __init__(self, uri):
        self.uri = uri

    def _split_hostname(self):
        parsed = urlsplit(self.uri)
        return parsed.netloc

    def _split_domain(self):
        ext = tldextract.extract(self.uri)
        domain = "{0}.{1}".format(ext.domain, ext.suffix)
        return domain
