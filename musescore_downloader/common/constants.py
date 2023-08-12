from typing import Literal

"""Dictionary that maps a MIME type to a corresponding file extension
"""
content_type_to_extension: dict[Literal["image/png", "image/svg+xml"], str] = {
    "image/png": ".png",
    "image/svg+xml": ".svg"
}
