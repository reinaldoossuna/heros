from dataclasses import dataclass, field, fields
from pathlib import Path

import typst

from heros.config import settings


@dataclass
class Template:
    path: Path

    def asdict(self) -> dict[str, str]:
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            match value:
                case float():
                    result[f.name] = f"{value:.2f}"
                case str():
                    result[f.name] = value
                case Path():
                    result[f.name] = f"{value}"
                case _:
                    result[f.name] = f"{value}"
        return result

    def make_file(self, output: Path | None = None):
        return typst.compile(input=self.path, sys_inputs=self.asdict(), output=output)


@dataclass
class DefaultTemplate(Template):
    temp_min: float
    temp_max: float
    precip_total: float
    days_wo_rain: float

    path: Path = field(init=False, default=Path(settings.report_template))
