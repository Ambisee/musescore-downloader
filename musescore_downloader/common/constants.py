from typing import Literal

from reportlab.lib.pagesizes import (
    A4,
    LETTER,
)

content_type_to_extension: dict[Literal["image/png", "image/svg+xml"], str] = {
    "image/png": ".png",
    "image/svg+xml": ".svg"
}

pagesize_alias_to_value: dict[Literal["A4", "LETTER"], tuple[float, float]] = {
    'A4': A4,
    'LETTER': LETTER
}
