# -*- coding: utf-8 -*-
"""WebKit timestamp implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface


class WebKitTime(interface.DateTimeValues):
  """WebKit timestamp.

  The WebKit timestamp is a signed 64-bit integer that contains the number of
  micro seconds since 1601-01-01 00:00:00.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
  """

  # The difference between Jan 1, 1601 and Jan 1, 1970 in seconds.
  _WEBKIT_TO_POSIX_BASE = 11644473600

  def __init__(self, timestamp=None):
    """Initializes a WebKit timestamp.

    Args:
      timestamp (Optional[int]): WebKit timestamp.
    """
    super(WebKitTime, self).__init__()
    self.precision = definitions.PRECISION_1_MICROSECOND
    self.timestamp = timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a WebKit timestamp from a date and time string.

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

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self.timestamp += self._WEBKIT_TO_POSIX_BASE
    self.timestamp *= definitions.MICROSECONDS_PER_SECOND
    self.timestamp += date_time_values.get('microseconds', 0)

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the WebKit timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if (self.timestamp is None or self.timestamp < self._INT64_MIN or
        self.timestamp > self._INT64_MAX):
      return None, None

    timestamp, microseconds = divmod(
        self.timestamp, definitions.MICROSECONDS_PER_SECOND)
    timestamp -= self._WEBKIT_TO_POSIX_BASE
    return timestamp, microseconds * self._100NS_PER_MICROSECOND

  def CopyToDateTimeString(self):
    """Copies the WebKit timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######
    """
    if (self.timestamp is None or self.timestamp < self._INT64_MIN or
        self.timestamp > self._INT64_MAX):
      return

    timestamp, microseconds = divmod(
        self.timestamp, definitions.MICROSECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValues(
        number_of_days, 1601, 1, 1)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds, microseconds)

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if (self.timestamp is None or self.timestamp < self._INT64_MIN or
        self.timestamp > self._INT64_MAX):
      return

    return self.timestamp - (
        self._WEBKIT_TO_POSIX_BASE * definitions.MICROSECONDS_PER_SECOND)
