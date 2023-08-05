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
        self.baseline = pendulum.instance(baseline)
        self.seconds = seconds

    def __repr__(self):
        return u'<AnyTimestamp {} +/- {} secs>'.format(
            self.baseline.isoformat(), self.seconds
        )

    def __eq__(self, other):
        other_local = pendulum.parse(other)
        difference = other_local.diff(self.baseline).total_seconds()
        return abs(difference) <= self.seconds

