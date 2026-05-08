"""Shared utility helpers."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any


TRUE_VALUES = {"true", "yes", "y", "1", "completed", "complete", "done", "high"}
FALSE_VALUES = {"false", "no", "n", "0", "not completed", "incomplete", "pending", "low"}


def normalize_text(value: Any) -> str:
    """Return a stripped lowercase string for comparisons."""
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""
    return text.lower()


def clean_text(value: Any, fallback: str = "") -> str:
    """Return display-ready text with blanks normalized."""
    if value is None:
        return fallback
    text = str(value).strip()
    if text.lower() in {"nan", "none", "null", ""}:
        return fallback
    return text


def parse_date(value: Any) -> date | None:
    """Parse a CSV or YAML date value into a date."""
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    text = clean_text(value)
    if not text:
        return None
    return datetime.strptime(text, "%Y-%m-%d").date()


def days_between(start: date | None, end: date | None) -> int | None:
    """Return day distance from start to end."""
    if start is None or end is None:
        return None
    return (end - start).days


def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    """Clamp a score to a bounded range."""
    return max(minimum, min(maximum, value))


def as_bool(value: Any) -> bool:
    """Interpret common CSV truthy values."""
    text = normalize_text(value)
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    return False


def format_currency(value: Any) -> str:
    """Format an integer-ish value as USD without cents."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "$0"
    return f"${number:,.0f}"


def join_names(values: list[str], limit: int = 8) -> str:
    """Join account names for compact CSV cells."""
    cleaned = [clean_text(value) for value in values if clean_text(value)]
    if len(cleaned) <= limit:
        return "; ".join(cleaned)
    remaining = len(cleaned) - limit
    return "; ".join(cleaned[:limit]) + f"; plus {remaining} more"


def weighted_average(factors: dict[str, float], weights: dict[str, Any]) -> float:
    """Calculate a weighted average using only available factor names."""
    total_weight = sum(float(weights[name]) for name in factors)
    if total_weight <= 0:
        return 0
    return sum(float(factors[name]) * float(weights[name]) for name in factors) / total_weight
