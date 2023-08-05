from urllib.parse import urlencode


def url_params(params):
    return "" if not params else "?" + urlencode(params)
