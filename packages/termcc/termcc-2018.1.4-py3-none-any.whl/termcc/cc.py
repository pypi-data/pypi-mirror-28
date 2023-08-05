# -*- coding: UTF-8 -*-



import re
import sys

from termcc.unicodes_codec import UNICODE_TERMCC, TERMCC_ALIAS_UNICODE, TERMCC_UNICODE

__all__ = ['cc', 'dc', 'get_termcc_regexp']

PY2 = sys.version_info[0] is 2

_TERMCC_REGEXP = None
_DEFAULT_DELIMITER = ":"


def cc(string, use_aliases=False, delimiters=(_DEFAULT_DELIMITER, _DEFAULT_DELIMITER)):

    pattern = re.compile(u'(%s[a-zA-Z0-9\+\-_&.ô’Åéãíç()!#*]+%s)' % delimiters)

    def replace(match):
        mg = match.group(1).replace(delimiters[0], _DEFAULT_DELIMITER).replace(delimiters[1], _DEFAULT_DELIMITER)
        if use_aliases:
            return TERMCC_ALIAS_UNICODE.get(mg, mg)
        else:
            return TERMCC_UNICODE.get(mg, mg)

    return pattern.sub(replace, string)


def dc(string, delimiters=(_DEFAULT_DELIMITER, _DEFAULT_DELIMITER)):

    def replace(match):
        val = UNICODE_TERMCC.get(match.group(0), match.group(0))
        return delimiters[0] + val[1:-1] + delimiters[1]

    return get_termcc_regexp().sub(replace, string)


def get_termcc_regexp():

    global _TERMCC_REGEXP
    if _TERMCC_REGEXP is None:
        emojis = sorted(TERMCC_UNICODE.values(), key=len,
                        reverse=True)
        pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
        _TERMCC_REGEXP = re.compile(pattern)
    return _TERMCC_REGEXP


