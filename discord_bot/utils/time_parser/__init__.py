from __future__ import absolute_import
from codecs import open
from os import path

try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding="utf-8") as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (running code interactively?)'
except IOError as e:
    __version__ = 'unknown (%s)' % e

from .ParseTime import parse_time as parse