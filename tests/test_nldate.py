from nldate.parse import parse
from datetime import date, timedelta


def test_today_mdy():
    assert parse("January 15, 2024") == date(2024, 1, 15)


def test_today_ymd():
    assert parse("2024 August 15") == date(2024, 8, 15)


def test_today_dmy():
    assert parse("15 January, 2008") == date(2008, 1, 15)


def test_today_mdy_abbrev():
    assert parse("Jan 15, 2024") == date(2024, 1, 15)


def test_today_mdy_abbrev_no_comma():
    assert parse("Jan 15 2024") == date(2024, 1, 15)


def test_iso_today():
    assert parse("2025-03-28") == date(2025, 3, 28)


def test_iso_today_day_zero_padded():
    assert parse("2025-12-04") == date(2025, 12, 4)


def test_numbers_slash_today():
    assert parse("2026/05/19") == date(2026, 5, 19)


def test_numbers_slash_not_zero_padded_today():
    assert parse("2023/11/15") == date(2023, 11, 15)


def test_n_days_before():
    assert parse("eight days before April 17, 2019") == date(2019, 4, 9)


def test_n_days_before_n_as_number():
    assert parse("16 days before January 3, 1978") == date(1977, 12, 18)


def test_n_weeks_after():
    assert parse("three weeks after January 15, 2024") == date(2024, 2, 5)


def test_next_weekday_today_passed():
    assert parse("next friday", today=date(2026, 5, 13)) == date(2026, 5, 22)


def test_in_n_days_today_passed():
    assert parse("in four days", today=date(2026, 5, 13)) == date(2026, 5, 17)


def test_in_n_days_today_default():
    curr_date = date.today()
    assert parse("in seven days", today=curr_date) == curr_date + timedelta(days=7)


def test_n_months_after():
    assert parse("five months after today", today=date(1988, 3, 13)) == date(
        1988, 8, 13
    )


def test_in_n_days_from():
    assert parse("four days from today", today=date(2026, 5, 13)) == date(2026, 5, 17)


def test_in_n_days_from_tomorrow():
    assert parse("four days from tomorrow", today=date(2026, 5, 13)) == date(
        2026, 5, 18
    )


def test_in_n_days_from_the_day_after_tomorrow():
    assert parse(
        "seven days from the day after tomorrow", today=date(2026, 5, 13)
    ) == date(2026, 5, 22)


def test_in_n_days_from_yesterday():
    assert parse("four days from yesterday", today=date(2026, 5, 13)) == date(
        2026, 5, 16
    )


def test_in_n_days_before_yesterday():
    assert parse("four days before yesterday", today=date(2026, 5, 13)) == date(
        2026, 5, 8
    )


def test_in_n_days_before_the_day_before_yesterday():
    assert parse(
        "four days before the day before yesterday", today=date(2026, 5, 13)
    ) == date(2026, 5, 7)
