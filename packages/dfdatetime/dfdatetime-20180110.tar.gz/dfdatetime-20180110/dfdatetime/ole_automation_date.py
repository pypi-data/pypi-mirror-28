# -*- coding: utf-8 -*-
"""OLE automation date (or Floatingtime or Application time) implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface


class OLEAutomationDate(interface.DateTimeValues):
  """OLE Automation date.

  The OLE Automation date is a floating point value that contains the number of
  days since 1899-12-30 (also known as the OLE Automation date epoch), and the
  fractional part represents the fraction of a day since midnight. Negative
  values represent date and times predating the OLE Automation date epoch.

  Also see:
    https://msdn.microsoft.com/en-us/library/system.datetime.tooadate(v=vs.110).aspx

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (float): OLE Automation date.
  """
  # The difference between Dec 30, 1899 and Jan 1, 1970 in days.
  _OLE_AUTOMATION_DATE_TO_POSIX_BASE = 25569

  def __init__(self, timestamp=None):
    """Initializes an OLE Automation date.

    Args:
      timestamp (Optional[float]): OLE Automation date.
    """
    super(OLEAutomationDate, self).__init__()
    self.precision = definitions.PRECISION_1_MICROSECOND
    self.timestamp = timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies an OLE Automation date from a date and time string.

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

    timestamp = float(timestamp)
    if microseconds is not None:
      timestamp += float(microseconds) / definitions.MICROSECONDS_PER_SECOND

    timestamp /= definitions.SECONDS_PER_DAY
    timestamp += self._OLE_AUTOMATION_DATE_TO_POSIX_BASE

    self.timestamp = timestamp
    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the OLE Automation date to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self.timestamp is None:
      return None, None

    timestamp = self.timestamp - self._OLE_AUTOMATION_DATE_TO_POSIX_BASE
    timestamp *= definitions.SECONDS_PER_DAY
    remainder = int((timestamp % 1) * self._100NS_PER_SECOND)
    return int(timestamp), remainder

  def CopyToDateTimeString(self):
    """Copies the OLE Automation date to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######
    """
    if self.timestamp is None:
      return

    timestamp = self.timestamp * definitions.SECONDS_PER_DAY

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        int(timestamp))

    year, month, day_of_month = self._GetDateValues(
        number_of_days, 1899, 12, 30)

    microseconds = int((timestamp % 1) * definitions.MICROSECONDS_PER_SECOND)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds, microseconds)

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self.timestamp is None:
      return

    timestamp = self.timestamp - self._OLE_AUTOMATION_DATE_TO_POSIX_BASE
    timestamp *= definitions.SECONDS_PER_DAY
    timestamp *= definitions.MICROSECONDS_PER_SECOND
    return int(timestamp)
