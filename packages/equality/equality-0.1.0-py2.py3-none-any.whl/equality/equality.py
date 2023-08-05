# coding: utf-8
"""
Equality test utilities.
"""
import datetime
import re

import pendulum

class AnyBase(object):
    """
    Base class.
    """
    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<{}>'.format(type(self).__name__)


class AnyInt(AnyBase):
    """
    Compares equal to any integer.
    """
    def __eq__(self, other):
        return isinstance(other, int)


class AnyTimestamp(AnyBase):
    """
    Compares equal to a string timestamp that is within a given number of
    seconds from a given datetime. eg:

        d1 = datetime(2017, 12, 31, 23, 59, 00)
        d2 = datetime(2017, 12, 31, 23, 59, 10) # ten seconds later
        AnyTimestamp(d1, seconds=10) == d2.isoformat() # True
        AnyTimestamp(d1, seconds=9) == d2.isoformat() # False
    """
    def __init__(self, baseline, seconds=10):
        """
        baseline: A datetime to compare against (no tz is assumed to be UTC)
        seconds: A number of seconds leeway for the approximate comparison.
        """
        self.baseline = pendulum.instance(baseline, tz=baseline.tzinfo)
        self.seconds = seconds

    def __repr__(self):
        return u'<AnyTimestamp {} +/- {} secs>'.format(
            self.baseline.isoformat(), self.seconds
        )

    def __eq__(self, other):
        other_local = self.apply_tz_offset(
            self.parse_timestamp(other),
            self.parse_tz_offset(other),
        )
        difference = (self.baseline - other_local).total_seconds()
        return abs(difference) <= self.seconds

    def parse_timestamp(self, stamp_tz):
        """
        Given a timestamp in the format
        yyyy-mm-ddThh:mm:ss-HH:MM
        strips the trailing timezone portion,
        and returns the rest as a naive datetime.
        """
        assert len(stamp_tz) == 25
        return pendulum.parse(stamp_tz[:19])

    def parse_tz_offset(self, stamp_tz):
        """
        Given a timestamp in the format
        yyyy-mm-ddThh:mm:ss[+-]HH:MM
        returns the trailing '+HH:MM' or [-HH:MM] as integer hour offset.
        Non-integer hour offsets are not handled and raise assertion error.
        """
        tz = stamp_tz[-6:]
        VALID_TZ = '([+-]\d\d):00$'
        match = re.match(VALID_TZ, tz)
        assert match, 'Bad timezone "{}"'.format(tz)
        return int(match.groups()[0])

    def apply_tz_offset(self, naive_timestamp, tz_offset):
        return naive_timestamp.in_timezone(tz_offset)

