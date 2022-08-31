from dataclasses import dataclass
from typing import List
from typing import Optional


@dataclass
class RecordExtensions:
    code: List[str]


@dataclass
class BRecord:
    # Unix timestamp of the GPS fix in milliseconds
    timestamp: int

    # UTC time of the GPS fix in ISO 8601 format
    time: str

    latitude: int
    longitude: int
    valid: bool
    pressureAltitude: Optional[int]
    gpsAltitude: Optional[int]

    extensions: RecordExtensions

    fixAccuracy: Optional[int]

    # Engine Noise Level from 0.0 to 1.0
    enl: Optional[float]


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
