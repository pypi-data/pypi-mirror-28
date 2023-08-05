# -*- coding: utf-8 -*-
"""HFS timestamp implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface


class HFSTime(interface.DateTimeValues):
  """HFS timestamp.

  The HFS timestamp is an unsigned 32-bit integer that contains the number of
  seconds since 1904-01-01 00:00:00. Where in HFS the timestamp is typically
  in local time and in HFS+/HFSX in UTC.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (int): HFS timestamp.
  """
  # The difference between Jan 1, 1904 and Jan 1, 1970 in seconds.
  _HFS_TO_POSIX_BASE = 2082844800
  _UINT32_MAX = (1 << 32) - 1

  def __init__(self, timestamp=None):
    """Initializes a HFS timestamp.

    Args:
      timestamp (Optional[int]): HFS timestamp.
    """
    super(HFSTime, self).__init__()
    self.precision = definitions.PRECISION_1_SECOND
    self.timestamp = timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a HFS timestamp from a date and time string.

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

    if year < 1904 or year > 2040:
      raise ValueError('Year value not supported.')

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self.timestamp += self._HFS_TO_POSIX_BASE

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the HFS timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT32_MAX):
      return None, None

    timestamp = self.timestamp - self._HFS_TO_POSIX_BASE
    return timestamp, 0

  def CopyToDateTimeString(self):
    """Copies the HFS timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT32_MAX):
      return

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        self.timestamp)

    year, month, day_of_month = self._GetDateValues(
        number_of_days, 1904, 1, 1)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(
        year, month, day_of_month, hours, minutes, seconds)

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT32_MAX):
      return

    timestamp = self.timestamp - self._HFS_TO_POSIX_BASE
    return timestamp * definitions.MICROSECONDS_PER_SECOND
