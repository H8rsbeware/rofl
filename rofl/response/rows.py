from dataclasses import dataclass
from collections.abc import Iterable

from ..constants import ROW_DELIMITER, UNIT_SEPARATOR, NUL


@dataclass(frozen=True)
class RofiRow:
    value: str
    display: str | None = None
    icon: list[str] | str | None = None
    meta: list[str] | str | None = None
    info: str | None = None
    urgent: bool = False
    active: bool = False
    nonselectable: bool = False
    permanent: bool = False

    def render(self, *, delim: str = ROW_DELIMITER) -> str:
        options: list[tuple[str, str]] = []

        self._append_string(options, "display", self.display)

        normalised_icon = self.icon
        if not isinstance(normalised_icon, list):
            normalised_icon = [normalised_icon] if normalised_icon is not None else []
        self._append_str_list(options, "icon", normalised_icon, ",")

        normalised_meta = self.meta
        if not isinstance(normalised_meta, list):
            normalised_meta = [normalised_meta] if normalised_meta is not None else []
        self._append_str_list(options, "meta", normalised_meta, " ")

        self._append_string(options, "info", self.info)
        self._append_bool(options, "urgent", self.urgent)
        self._append_bool(options, "active", self.active)
        self._append_bool(options, "nonselectable", self.nonselectable)
        self._append_bool(options, "permanent", self.permanent)

        if not options:
            return f"{self.value}{delim}"

        encoded = UNIT_SEPARATOR.join(
            part for name, value in options for part in (name, value)
        )

        return f"{self.value}{NUL}{encoded}{delim}"

    @staticmethod
    def _append_string(options: list[tuple[str, str]], name: str, value: str | None):
        if value is not None:
            options.append((name, value))

    @staticmethod
    def _append_bool(options: list[tuple[str, str]], name: str, value: bool | None):
        if value is None:
            return

        options.append((name, "true" if value else "false"))

    @staticmethod
    def _append_str_list(
        options: list[tuple[str, str]],
        name: str,
        value: list[str] | None,
        join_with: str,
    ):
        if value is None:
            return

        compressed = join_with.join(value)
        options.append((name, compressed))
