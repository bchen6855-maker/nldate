from __future__ import annotations

import re
from datetime import date, timedelta

MONTH_NAMES: dict[str, int] = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

WEEKDAY_NAMES: dict[str, int] = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}

WORD_NUMBERS: dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}


def _parse_number(s: str) -> int | None:
    if s.isdigit():
        return int(s)
    return WORD_NUMBERS.get(s)


def _add_months(d: date, n: int) -> date:
    total_months = d.month - 1 + n
    year = d.year + total_months // 12
    month = total_months % 12 + 1
    month_days = [
        0,
        31,
        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    day = min(d.day, month_days[month])
    return date(year, month, day)


def _parse_absolute(s: str) -> date | None:
    s = s.strip()

    m = re.match(r"(\w+)\.? (\d{1,2})(?:st|nd|rd|th)?,? (\d{4})$", s)
    if m:
        word, day_str, year_str = m.groups()
        month = MONTH_NAMES.get(word.lower().rstrip("."))
        if month:
            return date(int(year_str), month, int(day_str))

    m = re.match(r"(\d{1,2})(?:st|nd|rd|th)? (\w+)\.?,? (\d{4})$", s)
    if m:
        day_str, word, year_str = m.groups()
        month = MONTH_NAMES.get(word.lower().rstrip("."))
        if month:
            return date(int(year_str), month, int(day_str))

    m = re.match(r"(\d{4}) (\w+)\.? (\d{1,2})(?:st|nd|rd|th)?$", s)
    if m:
        year_str, word, day_str = m.groups()
        month = MONTH_NAMES.get(word.lower().rstrip("."))
        if month:
            return date(int(year_str), month, int(day_str))

    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})$", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})$", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    return None


def _parse_date_ref(s: str, today: date) -> date | None:
    s = s.strip().lower()

    if s == "today":
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)
    if s == "yesterday":
        return today - timedelta(days=1)
    if s == "the day after tomorrow":
        return today + timedelta(days=2)
    if s == "the day before yesterday":
        return today - timedelta(days=2)

    return _parse_absolute(s)


def _parse_relative(s: str, today: date) -> date:
    s_lower = s.lower().strip()

    m = re.match(r"^next (\w+)$", s_lower)
    if m:
        weekday_name = m.group(1)
        target = WEEKDAY_NAMES.get(weekday_name)
        if target is not None:
            current = today.weekday()
            days_ahead = target - current + 7
            return today + timedelta(days=days_ahead)

    m = re.match(r"^in (\w+) (days?|weeks?|months?)$", s_lower)
    if m:
        n = _parse_number(m.group(1))
        unit = m.group(2)
        if n is not None:
            if unit.startswith("day"):
                return today + timedelta(days=n)
            if unit.startswith("week"):
                return today + timedelta(weeks=n)
            if unit.startswith("month"):
                return _add_months(today, n)

    m = re.match(r"^(\w+) (days?|weeks?|months?) (before|after|from) (.+)$", s_lower)
    if m:
        n = _parse_number(m.group(1))
        unit = m.group(2)
        direction = m.group(3)
        ref_str = m.group(4)
        if n is not None:
            base = _parse_date_ref(ref_str, today)
            if base is not None:
                if unit.startswith("month"):
                    return _add_months(base, n if direction != "before" else -n)
                delta = n * 7 if unit.startswith("week") else n
                if direction == "before":
                    return base - timedelta(days=delta)
                return base + timedelta(days=delta)

    raise ValueError(f"Unable to parse date: {s}")


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    result = _parse_absolute(s)
    if result is not None:
        return result

    return _parse_relative(s, today)
