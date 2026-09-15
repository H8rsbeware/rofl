import os
import sys

from dataclasses import dataclass
from collections.abc import Mapping, Sequence

from .type import RofiRequestType


@dataclass(frozen=True)
class RofiRequest:
    event: RofiRequestType
    raw_event_input: int
    accepted_text: str | None
    data: str | None
    custom_key: int | None
    info: str | None
    input_text: str | None

    @classmethod
    def from_environment(
        cls,
        argv: Sequence[str] | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> "RofiRequest":
        if environ == None:
            environ = os.environ

        retv = environ.get("ROFI_RETV", "0")
        rtype, raw_input, custom_key = RofiRequestType.identifyRETV(retv)

        sel_text: str | None = None
        if argv == None:
            argv = sys.argv

        if len(argv) > 1:
            sel_text = argv[1]

        return RofiRequest(
            event=rtype,
            raw_event_input=raw_input,
            accepted_text=sel_text,
            custom_key=custom_key,
            data=environ.get("ROFI_DATA"),
            info=environ.get("ROFI_INFO"),
            input_text=environ.get("ROFI_INPUT"),
        )
