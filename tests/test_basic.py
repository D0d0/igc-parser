import unittest

from src.parser import ARecord
from src.parser import IgcParser


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

        line = "AXSX001 SKYTRAXX V1.60 SN:2726125672"
        record: ARecord = IgcParser._parse_a_record(line)
        self.assertIsNone(record.num_flight)
        self.assertEqual(record.manufacturer, "XSX")
        self.assertIsNone(record.logger_id)
        self.assertEqual(record.additional_data, "001 SKYTRAXX V1.60 SN:2726125672")
