# -*- coding: utf-8 -*-
"""Cocoa timestamp implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface


class CocoaTime(interface.DateTimeValues):
  """Cocoa timestamp.

  The Cocoa timestamp is a floating point value that contains the number of
  seconds since 2001-01-01 00:00:00 (also known as the Cocoa epoch).
  Negative values represent date and times predating the Cocoa epoch.

  Also see:
    https://developer.apple.com/library/ios/documentation/cocoa/Conceptual/
        DatesAndTimes/Articles/dtDates.html

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (float): Cocoa timestamp.
  """
  # The difference between Jan 1, 2001 and Jan 1, 1970 in seconds.
  _COCOA_TO_POSIX_BASE = -978307200

  def __init__(self, timestamp=None):
    """Initializes a Cocoa timestamp.

    Args:
      timestamp (Optional[float]): Cocoa timestamp.
    """
    super(CocoaTime, self).__init__()
    self.precision = definitions.PRECISION_1_SECOND
    self.timestamp = timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a Cocoa timestamp from a date and time string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get('year', 0)
    month = date_time_values.get('month', 0)
    day_of_month = date_time_values.get('day_of_month', 0)
    hours = date_time_values.get('hours', 0)
    minutes = date_time_values.get('minutes', 0)
    seconds = date_time_values.get('seconds', 0)
    microseconds = date_time_values.get('microseconds', None)

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp += self._COCOA_TO_POSIX_BASE

    timestamp = float(timestamp)
    if microseconds is not None:
      timestamp += float(microseconds) / definitions.MICROSECONDS_PER_SECOND

    self.timestamp = timestamp
    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the Cocoa timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self.timestamp is None:
      return None, None

    timestamp = self.timestamp - self._COCOA_TO_POSIX_BASE
    remainder = int((timestamp % 1) * self._100NS_PER_SECOND)
    return int(timestamp), remainder

  def CopyToDateTimeString(self):
    """Copies the Cocoa timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######
    """
    if self.timestamp is None:
      return

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        int(self.timestamp))

    year, month, day_of_month = self._GetDateValues(
        number_of_days, 2001, 1, 1)

    microseconds = int(
        (self.timestamp % 1) * definitions.MICROSECONDS_PER_SECOND)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds, microseconds)

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self.timestamp is None:
      return

    timestamp = definitions.MICROSECONDS_PER_SECOND * (
        self.timestamp - self._COCOA_TO_POSIX_BASE)
    return int(timestamp)
