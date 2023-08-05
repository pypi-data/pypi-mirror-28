#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Cocoa timestamp implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import cocoa_time


class CocoaTimeTest(unittest.TestCase):
  """Tests for the Cocoa timestamp."""

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    cocoa_time_object = cocoa_time.CocoaTime()

    expected_timestamp = 394934400.0
    cocoa_time_object.CopyFromDateTimeString('2013-07-08')
    self.assertEqual(cocoa_time_object.timestamp, expected_timestamp)

    expected_timestamp = 395011845.0
    cocoa_time_object.CopyFromDateTimeString('2013-07-08 21:30:45')
    self.assertEqual(cocoa_time_object.timestamp, expected_timestamp)

    expected_timestamp = 395011845.546875
    cocoa_time_object.CopyFromDateTimeString('2013-07-08 21:30:45.546875')
    self.assertEqual(cocoa_time_object.timestamp, expected_timestamp)

    expected_timestamp = 395015445.546875
    cocoa_time_object.CopyFromDateTimeString('2013-07-08 21:30:45.546875-01:00')
    self.assertEqual(cocoa_time_object.timestamp, expected_timestamp)

    expected_timestamp = 395008245.546875
    cocoa_time_object.CopyFromDateTimeString('2013-07-08 21:30:45.546875+01:00')
    self.assertEqual(cocoa_time_object.timestamp, expected_timestamp)

    expected_timestamp = 86400.0
    cocoa_time_object.CopyFromDateTimeString('2001-01-02 00:00:00')
    self.assertEqual(cocoa_time_object.timestamp, expected_timestamp)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.0)

    expected_stat_time_tuple = (1373319045, 0)
    stat_time_tuple = cocoa_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    cocoa_time_object = cocoa_time.CocoaTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = cocoa_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.546875)

    date_time_string = cocoa_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2013-07-08 21:30:45.546875')

    cocoa_time_object = cocoa_time.CocoaTime()

    date_time_string = cocoa_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    cocoa_time_object = cocoa_time.CocoaTime(timestamp=395011845.0)

    expected_micro_posix_timestamp = 1373319045000000
    micro_posix_timestamp = cocoa_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    cocoa_time_object = cocoa_time.CocoaTime()

    micro_posix_timestamp = cocoa_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
