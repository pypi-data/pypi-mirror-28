from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import inspect
import os
import pickle
import time
import zlib


def count_lines(filename):
    """
    counts how many lines a file has
    """
    result = sum(1 for _ in open(filename))
    return result


def millis(diff):
    """start and end are datetime instances"""
    ms = diff.days * 24 * 60 * 60 * 1000
    ms += diff.seconds * 1000
    ms += diff.microseconds / 1000
    return ms


def date_time_files():
    """converts a datetime value to a string you can use for a filename"""
    return datetime.datetime.now().timestamp()


def date_time_readable_file():
    """converts a datetime to a string value for filenames that you can read the date"""
    return time.strftime("%Y-%m-%d", time.gmtime())


def pickler(some_object, filename, compress=False, compression_level=-1):
    """makes a nice jar with some_object's pickle"""

    if compress:
        filename = '{0}.pickle.gz'.format(os.path.splitext(filename)[0])
        with open(filename, 'wb') as f:
            f.write(zlib.compress(pickle.dump(some_object, pickle.HIGHEST_PROTOCOL), compression_level))
    else:
        with open(filename, 'wb') as f:
            pickle.dump(some_object, f, pickle.HIGHEST_PROTOCOL)

    trace("Made a pickle jar on file:{0}".format(filename))


def unpickler(filename):
    """so easy to take pickles out of the jar!!!"""
    if os.path.splitext(filename)[1] == '.gz':
        with open(filename, 'rb') as f:
            compressed_data = zlib.decompress(f.read())
            data = pickle.load(compressed_data)
            return data
    else:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            return data


def trace(msg=''):
    """Log compulsively everything"""
    if os.path.exists('trace-on'):
        pass
    else:
        print('{1} {2}'.format(datetime.datetime.now(), inspect.stack()[1][3], msg))


def log(msg=''):
    """simply displays the message with the caller name and a time stamp"""
    global last_log

    delta = datetime.datetime.now() - last_log
    last_log = datetime.datetime.now()
    print('{0:10,.00f} {1} >=> {2}'.format(millis(delta), inspect.stack()[1][3], msg))


def retrieve_number(filename):
    """use to retrieve and save (persist function below) to create a control file based in numbers"""
    trace(filename)
    if not os.path.exists(filename):
        return 0
    with open(filename) as f:
        number = f.readline()
        return int(number)


def persist_number(filename, number):
    """saves one number to file - file will have only number"""
    trace('saving number {0} on file {1}'.format(number, filename))
    with open(filename, 'w') as f:
        f.write('{0}'.format(number))
    #    f.truncate()
    trace('File:{1} <- Persisted number:{0}'.format(filename, number))


last_log = datetime.datetime.now()

