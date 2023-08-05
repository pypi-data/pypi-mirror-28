class BittrexBase(object):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def base_url(self):
        raise NotImplemented
