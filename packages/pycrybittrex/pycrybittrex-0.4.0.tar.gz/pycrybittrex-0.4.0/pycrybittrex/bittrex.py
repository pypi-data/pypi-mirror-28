import os
from pycrybittrex.definitions import ApiVersion
from pycrybittrex.core import Bittrex11
from pycrybittrex.core import Bittrex20


def create_client(api_version=ApiVersion.V1_1, api_key=None, api_secret=None):
    api_key_main = api_key or os.environ['BTX_API_KEY']
    api_secret_main = api_secret or os.environ['BTX_API_SECRET']

    if api_version == ApiVersion.V1_1:
        return Bittrex11(api_key_main, api_secret_main)

    if api_version == ApiVersion.V2_0:
        return Bittrex20(api_key_main, api_secret_main)

    raise NotImplemented("api version is not supported")
