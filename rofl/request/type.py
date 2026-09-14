from enum import Enum, auto
from ..exceptions import RofiRequestException


class RofiRequestType(Enum):
    INITIAL = auto()
    SELECTED = auto()
    CUSTOM_INPUT = auto()
    DELETED = auto()
    CUSTOM_KEY = auto()

    @staticmethod
    def identifyRETV(retv: str) -> tuple[RofiRequestType, int, int | None]:
        reti = int(retv)

        if 10 <= reti <= 28:
            return (
                RofiRequestType.CUSTOM_KEY,
                reti,
                reti - 9,
            )  # reduce by 9, to get the 1-index input key.

        if reti == 0:
            return RofiRequestType.INITIAL, reti, None
        if reti == 1:
            return RofiRequestType.SELECTED, reti, None
        if reti == 2:
            return RofiRequestType.CUSTOM_INPUT, reti, None
        if reti == 3:
            return RofiRequestType.DELETED, reti, None

        raise RofiRequestException(
            f"ROFI_RETV was equal to '{retv}', must be 0-3 | 10-28"
        )
