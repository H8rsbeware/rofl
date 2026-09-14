from dataclasses import dataclass, asdict
from collections.abc import Iterable

from ..exceptions import RofiResponseOptionsException
from ..constants import ROW_DELIMITER, NUL, UNIT_SEPARATOR


@dataclass(frozen=True)
class RofiResponseOptions:
    # presentation
    prompt: str | None = None
    message: str | None = None
    markup_rows: bool | None = None

    # interaction
    no_custom: bool | None = None
    use_hot_keys: bool | None = None

    # continuity
    keep_selection: bool | None = None
    keep_filter: bool | None = None
    new_selection: int | None = None
    data: str | None = None

    # appearance/navigation
    theme: str | None = None
    switch_mode: str | None = None

    # lower-level protocol options
    delim: str | None = None
    urgent: Iterable[int | tuple[int, int]] | None = None
    active: Iterable[int | tuple[int, int]] | None = None

    def build(self) -> str:
        opts = asdict(self)
        builder = ""
        cdel = ROW_DELIMITER

        for k, v in opts.items():
            if v is None:
                continue

            if k == "delim":
                cdel = str(v)

            builder += RofiResponseOptions.render_mode_option(k, v, delim=cdel)

        return builder

    @staticmethod
    def render_mode_option(
        name: str,
        value: str | bool | list[int | tuple[int, int]],
        *,
        delim: str | None = ROW_DELIMITER,
    ) -> str:
        if isinstance(value, bool):
            encoded_value = "true" if value else "false"
        elif isinstance(value, list):
            encoded_value = RofiResponseOptions.collect_indexes(value)
        else:
            encoded_value = str(value)

        name = name.replace("_", "-")
        return f"{NUL}{name}{UNIT_SEPARATOR}{encoded_value}{delim}"

    def validate(self):
        if self.new_selection is not None and self.keep_selection is not True:
            raise RofiResponseOptionsException(
                "Rofi requires keep_selection=True for new_selection to be set"
            )

    def has_values(self) -> bool:
        return len(asdict(self).keys()) != 0

    @staticmethod
    def collect_indexes(idxs: Iterable[int | tuple[int, int]]) -> str:
        builder = ""
        for i, idx in enumerate(idxs):
            if i != 0:
                builder += ","

            if not isinstance(idx, tuple):
                builder += str(idx)
            elif len(idx) == 2 and idx[0] < idx[1]:
                builder += f"{idx[0]}:{idx[1]}"
            else:
                raise RofiResponseOptionsException(
                    "index for rofi must be ints or tuple[int, int] where 0 < 1"
                )

        return builder
