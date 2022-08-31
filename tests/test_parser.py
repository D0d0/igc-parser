import datetime
import unittest
from typing import List

from igcparser import ARecord
from igcparser import IgcParser
from igcparser.enums import BRecord
from igcparser.enums import RecordExtension


class ParserMethodCase(unittest.TestCase):
    def test_a_record(self):
        line = "ALXV4YT,FLIGHT:1"
        record: ARecord = IgcParser._parse_a_record(line)
        self.assertEqual(record.num_flight, 1)
        self.assertEqual(record.manufacturer, "LXV")
        self.assertEqual(record.logger_id, "4YT")
        self.assertIsNone(record.additional_data)

        line = "AFLA2NF"
        record: ARecord = IgcParser._parse_a_record(line)
        self.assertIsNone(record.num_flight)
        self.assertEqual(record.manufacturer, "FLA")
        self.assertEqual(record.logger_id, "2NF")
        self.assertIsNone(record.additional_data)

        line: str = "AXSX001 SKYTRAXX V1.60 SN:2726125672"
        record: ARecord = IgcParser._parse_a_record(line)
        self.assertIsNone(record.num_flight)
        self.assertEqual(record.manufacturer, "XSX")
        self.assertIsNone(record.logger_id)
        self.assertEqual(record.additional_data, "001 SKYTRAXX V1.60 SN:2726125672")

    def test_b_record(self):
        line: str = "B1117344818577N01806797EA007590085500210"
        record: BRecord = IgcParser._parse_b_record(line)
        self.assertEqual(record.time, datetime.time(hour=11, minute=17, second=34))
        self.assertEqual(record.latitude, 48.396166666666666)
        self.assertEqual(record.longitude, 18.232833333333332)
        self.assertEqual(record.pressure_altitude, 759)
        self.assertEqual(record.gps_altitude, 855)
        self.assertTrue(record.valid)

    def test_ij_record(self):
        line: str = "J020810WDI1115WVE"
        record_extensions: List[RecordExtension] = IgcParser._parse_ij_record(line)
        self.assertEqual(len(record_extensions), 2)
        self.assertEqual(record_extensions[0].code, "WDI")
        self.assertEqual(record_extensions[1].code, "WVE")
        self.assertEqual(record_extensions[0].start, 7)
        self.assertEqual(record_extensions[1].start, 10)
        self.assertEqual(record_extensions[0].length, 9)
        self.assertEqual(record_extensions[1].length, 14)
