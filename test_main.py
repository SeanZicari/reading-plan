import typing
from datetime import date

from main import Book, BooksOfBible, chapter_counts_per_day, reading_plan


def test_chapter_counts_per_day_returns_generator():
    assert isinstance(
        chapter_counts_per_day(typing.Any, typing.Any, 0), typing.Generator
    )


def test_chapter_counts_per_day_returns_one_day_one_chapter():
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 2)

    assert next(chapter_counts_per_day(start_date, end_date, 1)) == (start_date, 1)


def test_chapter_counts_per_day_returns_two_chapters_one_day():
    start_date = date(2021, 1, 1)
    end_date = date(2021, 1, 2)

    assert next(chapter_counts_per_day(start_date, end_date, 2)) == (start_date, 2)


def test_chapter_counts_per_day_spreads_two_chapters_over_two_days():
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 3)

    assert list(chapter_counts_per_day(start_date, end_date, 2)) == [
        (date(2020, 1, 1), 1),
        (date(2020, 1, 2), 1),
    ]


def test_chapter_counts_per_day_spreads_three_chapters_over_two_days():
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 3)

    assert list(chapter_counts_per_day(start_date, end_date, 3)) == [
        (date(2020, 1, 1), 2),
        (date(2020, 1, 2), 1),
    ]


def test_chapter_counts_per_day_works_with_a_larger_example():
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 4)

    assert list(chapter_counts_per_day(start_date, end_date, 5)) == [
        (date(2020, 1, 1), 2),
        (date(2020, 1, 2), 2),
        (date(2020, 1, 3), 1),
    ]


def test_reading_plan_returns_generator():
    assert isinstance(reading_plan(*[typing.Any] * 3), typing.Generator)


def test_reading_plan_outputs_one_chapter_one_day():
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 2)
    books = [Book(BooksOfBible.GENESIS, 1)]

    assert list(reading_plan(start_date, end_date, books)) == [
        ("Genesis 1", date(2022, 1, 1))
    ]
