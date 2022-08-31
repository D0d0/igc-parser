import datetime
from dataclasses import dataclass
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
class TaskPoint:
    latitude: int
    longitude: int
    name: str


@dataclass
class Task:
    declaration_date: str
    declaration_time: str
    declaration_timestamp: int

    flight_date: str
    task_number: int

    num_turnpoints: int
    comment: str

    points: List[TaskPoint]


@dataclass
class Flight:
    pass
