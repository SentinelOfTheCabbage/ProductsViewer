from enum import Enum


class EditDbError(Enum):
    EMPTY_FIELDS = 1
    INCORRECT_DATA = 2

    NO_PREV_STEP = 3
    NO_NEXT_STEP = 4
    NO_SELECTOR = 5
