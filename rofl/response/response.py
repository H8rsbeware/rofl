from dataclasses import dataclass, field

from ..constants import ROW_DELIMITER

from .options import RofiResponseOptions
from .rows import RofiRow


@dataclass(frozen=True)
class RofiResponse:
    rows: list[RofiRow] = field(default_factory=list)
    options: RofiResponseOptions = field(default_factory=lambda: RofiResponseOptions())

    def render(self):
        if not self.rows and not self.options.has_values():
            return ""

        self.options.validate()

        builder = self.options.build()
        delim = self.options.delim if self.options.delim is not None else ROW_DELIMITER

        for r in self.rows:
            builder += r.render(delim=delim)

        return builder

    @classmethod
    def close(cls) -> "RofiResponse":
        return cls()

    @classmethod
    def switch_mode(cls, mode: str) -> "RofiResponse":
        return cls(
            options=RofiResponseOptions(
                switch_mode=mode,
            )
        )
