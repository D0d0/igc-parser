import datetime
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
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
    extensions: Dict[str, str]
    pressure_altitude: Optional[int] = None
    gps_altitude: Optional[int] = None

    fix_accuracy: Optional[int] = None

    enl: Optional[float] = None


@dataclass
class ARecord:
    logger_manufacturer: str
    logger_id: Optional[str]
    num_flight: Optional[int]
    additional_data: Optional[str]


@dataclass
class KRecord:
    time: datetime.time
    extensions: Dict[str, str]


@dataclass
class TaskPoint:
    latitude: float
    longitude: float
    name: Optional[str]


@dataclass
class Task:
    declaration_date: datetime.date
    declaration_time: datetime.time

    flight_date: Optional[datetime.date]

    num_turnpoints: int
    comment: Optional[str]

    task_number: Optional[int]
    points: List[TaskPoint] = field(default_factory=list)


@dataclass
class Flight:
    logger_manufacturer: Optional[str] = None
    logger_id: Optional[str] = None
    task: Optional[Task] = None
    fixes: List[BRecord] = field(default_factory=list)
