__author__ = 'srwareham'

"""
Utility for downloading files.

"""

import urllib2
import contextlib
import time
import socket
import StringIO


def download_file(url, max_retries=3, pause=3, timeout=socket.getdefaulttimeout()):
    """
    Attempt to download a file given a url.
    Note: this includes support for context management
    ie:
    with download_file(url) as f:
        ...do something with f

    :param url: The url of the file to download
    :param max_retries: The maximum number of attempts to make (default=3)
    :param pause: The amount of time to wait in between attempts (default-3)
    :param timeout: The timeout threshold (default=system default)
    :return: A closing object containing a file-like object (does not return on failure)
    """
    while max_retries > 0:
        try:
            response = urllib2.urlopen(url, timeout=timeout)
            return contextlib.closing(response)
        except urllib2.URLError, e:
            print "Error: " + str(e.reason)
            print "Retrying in " + str(pause) + " seconds.."
            time.sleep(pause)
            max_retries -= 1
            if max_retries == 0:
                raise


# Yes totally redundant, but different implementations work depending on needs--will eventually unify
def simple_download(url, max_retries=3, pause=3, timeout=socket.getdefaulttimeout()):
    """
    Attempt to download a file given a url.
    Note: this reads the download into a StringIO object
    ie:

    :param url: The url of the file to download
    :param max_retries: The maximum number of attempts to make (default=3)
    :param pause: The amount of time to wait in between attempts (default-3)
    :param timeout: The timeout threshold (default=system default)
    :return: A StringIO object containing a file-like object (does not return on failure)
    """
    while max_retries > 0:
        try:
            response = urllib2.urlopen(url, timeout=timeout)
            return StringIO.StringIO(response.read())
        except urllib2.URLError, e:
            print "Error: " + str(e.reason)
            print "Retrying in " + str(pause) + " seconds.."
            time.sleep(pause)
            max_retries -= 1
            if max_retries == 0:
                raise


def download_files(urls, output_paths):
    """
    Downloads each url's file to its respective path

    If len(urls) != len(output_paths) only files with corresponding paths will be downloaded.

    :param urls: An iterable of urls to download
    :param output_paths: An iterable of paths to output files to
    :return:
    """
    for url, path in zip(urls, output_paths):
        with download_file(url) as ff:
            with open(path, 'wb') as out:
                out.write(ff.read())