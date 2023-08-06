import base64


def unicode_to_base64(string):
    """converts unicode to base64"""
    return base64.b64encode(string.encode()).decode('utf-8')


def base64_to_unicode(string):
    """Converts base64 to unicode."""
    return base64.b64decode(string).decode('utf-8')


def get_base_path(ip_address, url):
    # Remove scheme if present
    ip_address = ip_address.split('://')[-1].strip('/')
    # clean up url (leading or trailing or multiple '/')
    urls = filter(lambda p: p != '', url.split('/'))
    # Put everything back together
    return 'http://{}'.format(join_path(ip_address, *urls))


def join_path(base, *parts):
    _parts = '/'.join(parts)
    if base.endswith("/"):
        url = base + _parts
    else:
        url = base + '/' + _parts
    return url
