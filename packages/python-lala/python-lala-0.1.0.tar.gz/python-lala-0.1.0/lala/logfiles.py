import re
import time
import subprocess as sp
from datetime import datetime
import urllib
import os
import gzip
from io import BytesIO

import pygeoip
import pandas

from .conf import conf

if not os.path.exists(conf['geolite_path']):
    response = urllib.request.urlopen(conf['geolite_url'])
    geolite_gz = response.read()
    geolite_bites = BytesIO(geolite_gz)
    with gzip.open(geolite_bites, 'rb') as f:
        geolite_content = f.read()
    with open(conf['geolite_path'], 'wb') as f:
        f.write(geolite_content)

geoip = pygeoip.GeoIP(conf['geolite_path'])

def get_remote_file_content(filename='/var/log/nginx/access.log',
                            host='localhost', user='root', decode='utf8'):
    proc = sp.Popen(['ssh', '%s@%s' % (user, host), 'cat %s' % filename],
                    stderr=sp.PIPE, stdout=sp.PIPE)
    out, err = proc.communicate()
    if len(err):
        raise IOError(err)
    if decode is not None:
        out = out.decode(decode)
    return out

def logs_lines_to_dataframe(log_lines):
    """Return a dataframe of access log entries, from the lines of NGINX logs.

    The log_lines are a list of strings, each representing one access logged
    by NGINX.

    """
    regexpr = r'(.*) -(.*) - \[(.*)\] "(.*)" (\d+) (\d+) "(.*)" "(.*)"'
    regexpr = re.compile(regexpr)
    errored_lines = []
    records = []
    for i, line in enumerate(log_lines):
        match = re.match(regexpr, line)
        fields = ('IP', 'stuff', 'date', 'request', 'response', 'status',
                  'referrer', 'browser')
        if match is None:
            errored_lines.append(i)
        else:
            records.append(dict(zip(fields, match.groups())))
    dataframe = pandas.DataFrame.from_records(records)
    dataframe['parsed_date'] = [datetime.strptime(s, '%d/%b/%Y:%H:%M:%S %z')
                                for s in dataframe['date']]
    dataframe['timestamp'] = [x.timestamp() for x in dataframe['parsed_date']]
    fields = ['country_name', 'city', 'country_code3', 'latitude', 'longitude']
    d = {f: [] for f in fields}
    for ip in dataframe.IP:
        rec = geoip.record_by_addr(ip)
        for field in fields:
            d[field].append(rec[field])
    for field in fields:
        dataframe[field] = d[field]
    return dataframe, errored_lines

durations = {
    'second': 1,
    'minute': 60,
    'hour': 60 * 60,
    'day': 60 * 60 * 24,
    'week': 60 * 60 * 24 * 7,
    'month': 60 * 60 * 24 * 30,
    'year': 60 * 60 * 24 * 365,
}

def time_of_last(num, duration):
    """Returns the EPOCH time (in seconds) of XX ago (relative to the present).

    Examples
    --------

    >>> time_of_last(2, 'week') # => EPOCH time of two weeks ago
    >>> time_of_last(5, 'hour') # => EPOCH time of five hours ago
    """
    return time.time() - num * durations[duration]

def entries_last(dataframe, num, duration):
    """Returns the dataframe of the latest entries up to XX ago.

    Examples
    --------

    >>> # Filter out all entries more than 1 hour old
    >>> last_hour_dataframe = entries_last(dataframe, 1, 'hour')
    >>> # Filter out all entries more than 5 days old
    >>> last_days_dataframe = entries_last(dataframe, 5, 'days')
    """
    return dataframe[dataframe.timestamp >= time_of_last(num, duration)]
