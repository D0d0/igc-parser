import datetime
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional


@dataclass
class RecordExtension:
    code: str
    start: int
    length: int


@dataclass
class BRecord:
    # UTC time of the GPS fix in ISO 8601 format
    time: datetime.time

    latitude: float
    longitude: float
    valid: bool
    pressure_altitude: Optional[int] = None
    gps_altitude: Optional[int] = None

    extensions: Optional[RecordExtension] = None

    fix_accuracy: Optional[int] = None

    enl: Optional[float] = None


@dataclass
class ARecord:
    manufacturer: str
    logger_id: Optional[str]
    num_flight: Optional[int]
    additional_data: Optional[str]


@dataclass
class KRecord:
    time: datetime.time
    code: List[str]


@dataclass
class TaskPoint:
    latitude: int
    longitude: int
    name: str


@dataclass
class Task:
    declaration_date: datetime.date
    declaration_time: datetime.time

    flight_date: datetime.date

    num_turnpoints: int
    comment: Optional[str]

    task_number: Optional[int]
    points: List[TaskPoint] = field(default_factory=list)


@dataclass
class Flight:
    task: Optional[Task] = None
    fixes: List[BRecord] = field(default_factory=list)
