"""
Page format definitions for PDF generation.
All dimensions are in points (1 inch = 72 points).
"""

from typing import NamedTuple


class PageSize(NamedTuple):
    """Page size in points (width, height)."""
    width: float
    height: float
    name: str


# Standard page formats
PAGE_FORMATS = {
    'A4': PageSize(595.27, 841.89, 'A4'),  # 210mm x 297mm
    'A3': PageSize(841.89, 1190.55, 'A3'),  # 297mm x 420mm
    'A5': PageSize(419.53, 595.27, 'A5'),  # 148mm x 210mm
    'Letter': PageSize(612, 792, 'Letter'),  # 8.5" x 11"
    'Legal': PageSize(612, 1008, 'Legal'),  # 8.5" x 14"
    'Tabloid': PageSize(792, 1224, 'Tabloid'),  # 11" x 17"
}


def get_page_size(format_name: str) -> PageSize:
    """Get page size by format name."""
    return PAGE_FORMATS.get(format_name, PAGE_FORMATS['A4'])


def mm_to_points(mm: float) -> float:
    """Convert millimeters to points."""
    return mm * 72 / 25.4


def points_to_mm(points: float) -> float:
    """Convert points to millimeters."""
    return points * 25.4 / 72
