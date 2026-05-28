from enum import StrEnum


class ELTStatus(StrEnum):
    ACTUAL = 'ACTUAL'
    NOT_ACTUAL = 'NOT_ACTUAL'
    UPDATE = 'UPDATE'
    ERROR = 'ERROR'


class SystemType(StrEnum):
    AS = 'AS'
    FP = 'FP'
