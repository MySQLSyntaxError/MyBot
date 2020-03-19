import re

SIGN = r'(?P<sign>[+|-])?'
# YEARS      = r'(?P<years>\d+)\s*(?:ys?|yrs?.?|years?)'
# MONTHS     = r'(?P<months>\d+)\s*(?:mos?.?|mths?.?|months?)'
WEEKS = r'(?P<weeks>[\d.]+)\s*(?:w|wks?|weeks?)'
DAYS = r'(?P<days>[\d.]+)\s*(?:d|dys?|days?)'
HOURS = r'(?P<hours>[\d.]+)\s*(?:h|hrs?|hours?)'
MINS = r'(?P<mins>[\d.]+)\s*(?:m|(mins?)|(minutes?))'
SECS = r'(?P<secs>[\d.]+)\s*(?:s|secs?|seconds?)'
SEPARATORS = r'[,/]'
SECCLOCK = r':(?P<secs>\d{2}(?:\.\d+)?)'
MINCLOCK = r'(?P<mins>\d{1,2}):(?P<secs>\d{2}(?:\.\d+)?)'
HOURCLOCK = r'(?P<hours>\d+):(?P<mins>\d{2}):(?P<secs>\d{2}(?:\.\d+)?)'
DAYCLOCK = (r'(?P<days>\d+):(?P<hours>\d{2}):'
            r'(?P<mins>\d{2}):(?P<secs>\d{2}(?:\.\d+)?)')

OPT = lambda x: r'(?:{x})?'.format(x=x, SEPARATORS=SEPARATORS)
OPTSEP = lambda x: r'(?:{x}\s*(?:{SEPARATORS}\s*)?)?'.format(
    x=x, SEPARATORS=SEPARATORS)

TIMEFORMATS = [
    r'{WEEKS}\s*{DAYS}\s*{HOURS}\s*{MINS}\s*{SECS}'.format(
        # YEARS=OPTSEP(YEARS),
        # MONTHS=OPTSEP(MONTHS),
        WEEKS=OPTSEP(WEEKS),
        DAYS=OPTSEP(DAYS),
        HOURS=OPTSEP(HOURS),
        MINS=OPTSEP(MINS),
        SECS=OPT(SECS)),
    r'{MINCLOCK}'.format(
        MINCLOCK=MINCLOCK),
    r'{WEEKS}\s*{DAYS}\s*{HOURCLOCK}'.format(
        WEEKS=OPTSEP(WEEKS),
        DAYS=OPTSEP(DAYS),
        HOURCLOCK=HOURCLOCK),
    r'{DAYCLOCK}'.format(
        DAYCLOCK=DAYCLOCK),
    r'{SECCLOCK}'.format(
        SECCLOCK=SECCLOCK),
    # r'{YEARS}'.format(
    # YEARS=YEARS),
    # r'{MONTHS}'.format(
    # MONTHS=MONTHS),
]

COMPILED_SIGN = re.compile(r'\s*' + SIGN + r'\s*(?P<unsigned>.*)$')
COMPILED_TIMEFORMATS = [re.compile(r'\s*' + timefmt + r'\s*$', re.I)
                        for timefmt in TIMEFORMATS]

MULTIPLIERS = dict([
    # ('years',  60 * 60 * 24 * 365),
    # ('months', 60 * 60 * 24 * 30),
    ('weeks', 60 * 60 * 24 * 7),
    ('days', 60 * 60 * 24),
    ('hours', 60 * 60),
    ('mins', 60),
    ('secs', 1)
])


def _interpret_as_minutes(sval, mdict):
    if (sval.count(':') == 1
            and '.' not in sval
            and (('hours' not in mdict) or (mdict['hours'] is None))
            and (('days' not in mdict) or (mdict['days'] is None))
            and (('weeks' not in mdict) or (mdict['weeks'] is None))
            # and (('months' not in mdict) or (mdict['months'] is None))
            # and (('years' not in mdict) or (mdict['years'] is None))
    ):
        mdict['hours'] = mdict['mins']
        mdict['mins'] = mdict['secs']
        mdict.pop('secs')
        pass
    return mdict


def parse_time(sval, granularity='seconds'):
    match = COMPILED_SIGN.match(sval)
    sign = -1 if match.groupdict()['sign'] == '-' else 1
    sval = match.groupdict()['unsigned']
    for timefmt in COMPILED_TIMEFORMATS:
        match = timefmt.match(sval)
        if match and match.group(0).strip():
            mdict = _interpret_as_minutes(sval, mdict)
            if granularity == 'minutes':
                mdict = _interpret_as_minutes(sval, mdict)

            if all(v.isdigit() for v in list(mdict.values()) if v):
                return sign * sum([MULTIPLIERS[k] * int(v, 10) for (k, v) in list(mdict.items()) if v is not None])
            elif ('secs' not in mdict or
                      mdict['secs'] is None or
                      mdict['secs'].isdigit()):
                # we will return an integer
                return (
                        sign * int(sum([MULTIPLIERS[k] * float(v) for (k, v) in
                                        list(mdict.items()) if k != 'secs' and v is not None])) +
                        (int(mdict['secs'], 10) if mdict['secs'] else 0))
            else:
                # SECS is a float, we will return a float
                return sign * sum([MULTIPLIERS[k] * float(v) for (k, v) in
                                   list(mdict.items()) if v is not None])
