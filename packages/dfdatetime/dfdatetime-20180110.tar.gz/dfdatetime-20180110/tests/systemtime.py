#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the SYSTEMTIME structure implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import systemtime


class FiletimeTest(unittest.TestCase):
  """Tests for the SYSTEMTIME structure."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    systemtime_object = systemtime.Systemtime()
    self.assertIsNotNone(systemtime_object)

    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))
    self.assertIsNotNone(systemtime_object)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 20)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 142)

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 20, 6, 31))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(1500, 8, 4, 12, 20, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 13, 4, 12, 20, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 7, 12, 20, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 32, 20, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 24, 6, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 20, 61, 31, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 20, 6, 61, 142))

    with self.assertRaises(ValueError):
      systemtime.Systemtime(
          system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 1001))

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    systemtime_object = systemtime.Systemtime()

    expected_number_of_seconds = 1281571200
    systemtime_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        systemtime_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 0)
    self.assertEqual(systemtime_object.minutes, 0)
    self.assertEqual(systemtime_object.seconds, 0)
    self.assertEqual(systemtime_object.milliseconds, 0)

    expected_number_of_seconds = 1281647191
    systemtime_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        systemtime_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 21)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 0)

    expected_number_of_seconds = 1281647191
    systemtime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        systemtime_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 21)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 546)

    expected_number_of_seconds = 1281650791
    systemtime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        systemtime_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 22)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 546)

    expected_number_of_seconds = 1281643591
    systemtime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        systemtime_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(systemtime_object.year, 2010)
    self.assertEqual(systemtime_object.month, 8)
    self.assertEqual(systemtime_object.day_of_month, 12)
    self.assertEqual(systemtime_object.hours, 20)
    self.assertEqual(systemtime_object.minutes, 6)
    self.assertEqual(systemtime_object.seconds, 31)
    self.assertEqual(systemtime_object.milliseconds, 546)

    expected_number_of_seconds = -11644387200
    systemtime_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(
        systemtime_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(systemtime_object.year, 1601)
    self.assertEqual(systemtime_object.month, 1)
    self.assertEqual(systemtime_object.day_of_month, 2)
    self.assertEqual(systemtime_object.hours, 0)
    self.assertEqual(systemtime_object.minutes, 0)
    self.assertEqual(systemtime_object.seconds, 0)
    self.assertEqual(systemtime_object.milliseconds, 0)

    with self.assertRaises(ValueError):
      systemtime_object.CopyFromDateTimeString('1600-01-02 00:00:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    expected_stat_time_tuple = (1281643591, 1420000)
    stat_time_tuple = systemtime_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    systemtime_object = systemtime.Systemtime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = systemtime_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    date_time_string = systemtime_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.142')

    systemtime_object = systemtime.Systemtime()

    date_time_string = systemtime_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    systemtime_object = systemtime.Systemtime(
        system_time_tuple=(2010, 8, 4, 12, 20, 6, 31, 142))

    expected_micro_posix_number_of_seconds = 1281643591142000
    micro_posix_number_of_seconds = systemtime_object.GetPlasoTimestamp()
    self.assertEqual(
        micro_posix_number_of_seconds, expected_micro_posix_number_of_seconds)

    systemtime_object = systemtime.Systemtime()

    micro_posix_number_of_seconds = systemtime_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_number_of_seconds)


if __name__ == '__main__':
  unittest.main()
