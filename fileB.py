#!/usr/bin/python3
"""Get new file and compare changes."""
from multiprocessing.connection import Listener


# Could impliment all result string generation in a class.
def gen_desc(dict):
    """Generate description of new ap."""
    desc = """
{} is added to the list with SNR {} and channel {}.\n
""".format(dict.get('ssid'), dict.get('snr'), dict.get('channel'))
    return desc


def check_diff(do, dn):
    """Check and generate description of updated ap."""
    keys = ['snr', 'channel']
    diffs = ""
    for key in keys:
        if do[key] != dn[key]:
            diffs += """
{}'s {} has changed from {} to {}.\n
""".format(do['ssid'], key, do[key], dn[key])
    return diffs


def by_ids(aps):
    """Generate a dict from list of aps based on ssid."""
    ids = {}
    for ap in aps:
        ids[ap['ssid']] = ap
    return ids


def compare_ap(old, new):
    """Compare and get changes."""
    res = ""
    nids = by_ids(new)
    oids = by_ids(old)
    for sid in nids:
        if sid in oids:
            res += check_diff(oids[sid], nids[sid])
        else:
            res += gen_desc(nids[sid])
    for sid in oids:
        if sid not in nids:
            res += "{} is removed from the list.\n".format(sid)

    return res


address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'password')
conn = listener.accept()
print('connection accepted from', listener.last_accepted)
last_version = conn.recv()
while True:
    try:
        new_version = conn.recv()
        print(compare_ap(last_version, new_version), end="")
        last_version = new_version
    except KeyboardInterrupt:
        listener.close()
        break
