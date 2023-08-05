from enum import Enum


class Scope(Enum):
    PRIVATE = 1
    PUBLIC = 2


class OrderType(Enum):
    BUY = 1
    SELL = 2
    BOTH = 3


class ApiVersion(Enum):
    V1_1 = 1.1
    V2_0 = 2.0
