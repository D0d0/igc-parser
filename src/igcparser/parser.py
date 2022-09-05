import datetime
import re
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from .enums import ARecord
from .enums import BRecord
from .enums import Flight
from .enums import KRecord
from .enums import RecordExtension
from .enums import Task
from .enums import TaskPoint
from .regexes import RE_A
from .regexes import RE_A_1
from .regexes import RE_B
from .regexes import RE_HFDTE
from .regexes import RE_IJ
from .regexes import RE_K
from .regexes import RE_TASK
from .regexes import RE_TASKPOINT


class IgcParser:
    @staticmethod
    def parse(file_path: Union[str, Path]) -> Flight:
        path: Path = Path(file_path)

        if not path.exists():
            raise Exception("Path does not exist.")

        with open(path) as f:
            return IgcParser._parse_lines([line.strip() for line in f.readlines()])

    @staticmethod
    def _parse_lines(lines: List[str]) -> Flight:
        flight: Flight = Flight()
        data_extensions: List[RecordExtension] = []
        fix_extension: List[RecordExtension] = []

        for line in lines:
            if line.startswith("A"):
                a_record: ARecord = IgcParser._parse_a_record(line)
                flight.logger_id = a_record.logger_id
                flight.logger_manufacturer = a_record.logger_manufacturer

            if line.startswith("C"):
                IgcParser._parse_task_line(line, flight)

            if line.startswith("H"):
                IgcParser._parse_header(line)

            if line.startswith("B"):
                flight.fixes.append(IgcParser._parse_b_record(line, fix_extension))

            if line.startswith("K"):
                IgcParser.parse_k_record(line, data_extensions)

            if line.startswith("I"):
                fix_extension = IgcParser._parse_ij_record(line)

            if line.startswith("J"):
                data_extensions = IgcParser._parse_ij_record(line)

        return Flight()

    @staticmethod
    def _parse_latitude(dd: str, mm: str, mmm: str, ns: str) -> float:
        latitude_degrees: float = int(dd) + float(f"{mm}.{mmm}") / 60

        return -latitude_degrees if ns == "S" else latitude_degrees

    @staticmethod
    def _parse_longitude(ddd: str, mm: str, mmm: str, ew: str) -> float:
        latitude_degrees: float = int(ddd) + float(f"{mm}.{mmm}") / 60

        return -latitude_degrees if ew == "W" else latitude_degrees

    @staticmethod
    def _parse_b_record(line: str, fix_extensions: List[RecordExtension]) -> BRecord:
        if match := re.match(RE_B, line, flags=re.IGNORECASE):
            return BRecord(
                time=datetime.time(
                    hour=int(match.group(1)),
                    minute=int(match.group(2)),
                    second=int(match.group(3)),
                ),
                latitude=IgcParser._parse_latitude(match.group(4), match.group(5), match.group(6), match.group(7)),
                longitude=IgcParser._parse_longitude(match.group(8), match.group(9), match.group(10), match.group(11)),
                valid=match.group(12) == "A",
                pressure_altitude=None if match.group(13) == "0000" else int(match.group(13)),
                gps_altitude=None if match.group(14) == "0000" else int(match.group(14)),
                extensions={
                    extension.code: line[extension.start : extension.start + extension.length]
                    for extension in fix_extensions
                },
            )

        raise Exception(f"Invalid B record at line: {line}")

    @staticmethod
    def _parse_a_record(line: str) -> ARecord:
        if match := re.match(RE_A, line, flags=re.IGNORECASE):
            return ARecord(
                logger_manufacturer=match.group(1),
                logger_id=match.group(2),
                num_flight=int(match.group(3)) if match.group(3) else None,
                additional_data=match.group(4) or None,
            )

        if match := re.match(RE_A_1, line, flags=re.IGNORECASE):
            return ARecord(
                logger_manufacturer=match.group(1),
                logger_id=None,
                num_flight=None,
                additional_data=match.group(2) or None,
            )

        raise Exception(f"Failed to parse ARecord: {line}")

    @staticmethod
    def _parse_ij_record(line: str) -> List[RecordExtension]:
        result: List[RecordExtension] = []
        if match := re.match(RE_IJ, line, flags=re.IGNORECASE):
            num: int = int(match.group(1))
            if len(line) < 3 + num * 7:
                raise Exception

            for i in range(num):
                offset: int = 3 + i * 7
                result.append(
                    RecordExtension(
                        start=int(line[offset : offset + 2]) - 1,
                        length=int(line[offset + 2 : offset + 4]) - 1,
                        code=line[offset + 4 : offset + 7],
                    )
                )

        return result

    @staticmethod
    def parse_k_record(line: str, data_extensions: List[RecordExtension]) -> KRecord:
        if match := re.match(RE_K, line, flags=re.IGNORECASE):
            return KRecord(
                time=datetime.time(
                    hour=int(match.group(1)),
                    minute=int(match.group(2)),
                    second=int(match.group(3)),
                ),
                extensions={
                    extension.code: line[extension.start : extension.start + extension.length]
                    for extension in data_extensions
                },
            )

        raise Exception(f"Failed to parse KRecord line: {line}")

    @staticmethod
    def _parse_header(line: str):
        def _parse_date_header() -> Tuple[datetime.date, Optional[int]]:
            if match := re.match(RE_HFDTE, line, flags=re.IGNORECASE):
                century: str = "19" if match[3][0] in ("8", "9") else "20"

                num_flight: Optional[int] = int(match[4]) if match[4] else None
                return datetime.date(year=int(century + match[3]), month=int(match[2]), day=int(match[1])), num_flight

            raise Exception(f"Failed to parse date header: {line}")

        header_type: str = line[2:5]

        if header_type == "DTE":
            date, num_flight = _parse_date_header()

        if header_type == "PLT":
            pass

        pass

    @staticmethod
    def _parse_task_line(line: str, flight: Flight) -> None:
        def _parse_task() -> Task:
            if match := re.match(RE_TASK, line, flags=re.IGNORECASE):
                century: str = "19" if match.group(3)[0] in ("8", "9") else "20"

                flight_date: Optional[datetime.date] = None
                if match.group(7) != "00" or match.group(8) != "00" or match.group(9) != "00":
                    flight_date = datetime.date(
                        year=int(("19" if match.group(9)[0] in ("8", "9") else "20") + match.group(9)),
                        month=int(match.group(8)),
                        day=int(match.group(7)),
                    )

                return Task(
                    declaration_date=datetime.date(
                        year=int(century + match.group(3)), month=int(match.group(2)), day=int(match.group(1))
                    ),
                    declaration_time=datetime.time(
                        hour=int(match.group(4)), minute=int(match.group(5)), second=int(match.group(6))
                    ),
                    flight_date=flight_date,
                    task_number=int(match.group(10)) if match.group(10) != "0000" else None,
                    num_turnpoints=int(match.group(11)),
                    comment=match.group(12) or None,
                )

            raise Exception(f"Failed to parse header task line: {line}")

        def _parse_task_line() -> TaskPoint:
            if match := re.match(RE_TASKPOINT, line, flags=re.IGNORECASE):
                return TaskPoint(
                    latitude=IgcParser._parse_latitude(match.group(1), match.group(2), match.group(3), match.group(4)),
                    longitude=IgcParser._parse_longitude(
                        match.group(5), match.group(6), match.group(7), match.group(8)
                    ),
                    name=match.group(9) if match.group(9) else None,
                )

            raise Exception(f"Failed to parse task point line: {line}")

        if flight.task is None:
            flight.task = _parse_task()
        else:
            flight.task.points.append(_parse_task_line())
