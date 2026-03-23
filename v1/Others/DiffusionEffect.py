import enum
class DiffusionEffect(enum.IntEnum):
    ORIGIN = 0
    RECEIVED = 1
    NOT_RECEIVED = 2
    SPREADER = 3
    DISINTERESTED = 4