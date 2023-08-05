#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import codecs
import collections
import json

import six

__version__ = '0.0.18'


def regular_cast(original, *attempts):
    for atmpt in attempts:
        if not callable(atmpt):
            return atmpt
        try:
            return atmpt(original)
        except (TypeError, ValueError):
            pass
    return original


def smart_cast(value, default):
    """
    Cast to the same type as `default`;
    if fail, return default
    :param value:
    :param default:
    :return:
    """
    func = type(default)
    try:
        return func(value)
    except (TypeError, ValueError):
        return default


def numerify(s):
    return regular_cast(s, int, float)


def want_bytes(s, **kwargs):
    """
    :param s: 
    :param kwargs: key word arguments passed to str.encode(..)
    :return: 
    """
    if not isinstance(s, six.binary_type):
        s = s.encode(**kwargs)
    return s


def want_unicode(s, **kwargs):
    """
    :param s: 
    :param kwargs: key word arguments passed to bytes.decode(..)
    :return: 
    """
    if not isinstance(s, six.text_type):
        return s.decode(**kwargs)
    return s


def want_str(s, **kwargs):
    """
    :param s:
    :param kwargs: key word arguments passed to s.decode(..)
    :return:
    """
    if not isinstance(s, str):
        return s.decode(**kwargs)
    return s


def namedtuple_to_dict(nt):
    fields = getattr(nt, '_fields')
    return collections.OrderedDict(zip(fields, nt))


def represent(obj, params):
    """
    :param obj:
    :param params: a dict or list
    """
    c = obj.__class__.__name__
    if isinstance(params, dict):
        parts = ('{}={}'.format(k, repr(v)) for k, v in params.items())
    else:
        parts = ('{}={}'.format(k, repr(getattr(obj, k))) for k in params)
    s = ', '.join(parts)
    return '<{}({}) at {}>'.format(c, s, hex(id(obj)))


def indented_json_print(o, *args, **kwargs):
    # https://stackoverflow.com/a/12888081/2925169
    decode = codecs.getdecoder('unicode_escape')
    outstr = json.dumps(o, indent=4, sort_keys=True)
    print(decode(outstr)[0], *args, **kwargs)
