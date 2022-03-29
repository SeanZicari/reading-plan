import dataclasses
import enum
import sys
import typing
from datetime import date, timedelta
from pprint import pprint

import click
import dateparser


class BooksOfBible(enum.Enum):
    GENESIS = "Genesis"
    EXODUS = "Exodus"
    LEVITICUS = "Leviticus"
    NUMBERS = "Numbers"
    DEUTERONOMY = "Deuteronomy"
    JOSHUA = "Joshua"
    JUDGES = "Judges"
    RUTH = "Ruth"
    FIRST_SAMUEL = "1 Samuel"


@dataclasses.dataclass
class Book:
    book: BooksOfBible
    num_chapters: int


all_books = {
    BooksOfBible.GENESIS.value: Book(BooksOfBible.GENESIS, 50),
    BooksOfBible.EXODUS.value: Book(BooksOfBible.EXODUS, 40),
    BooksOfBible.LEVITICUS.value: Book(BooksOfBible.LEVITICUS, 27),
    BooksOfBible.NUMBERS.value: Book(BooksOfBible.NUMBERS, 36),
    BooksOfBible.DEUTERONOMY.value: Book(BooksOfBible.DEUTERONOMY, 34),
    BooksOfBible.JOSHUA.value: Book(BooksOfBible.JOSHUA, 24),
    BooksOfBible.JUDGES.value: Book(BooksOfBible.JUDGES, 21),
    BooksOfBible.RUTH.value: Book(BooksOfBible.RUTH, 4),
    BooksOfBible.FIRST_SAMUEL.value: Book(BooksOfBible.FIRST_SAMUEL, 31),
}


@dataclasses.dataclass
class Output:
    reading: str
    deadline: date


def chapters(books: typing.List[Book]):
    for book in books:
        for chapter in range(1, book.num_chapters + 1):
            yield f"{book.book.value} {chapter}"


def chapter_counts_per_day(start_date: date, end_date: date, total_chapters: int):
    num_days = (end_date - start_date).days
    chapters_per_day = total_chapters // num_days
    extra_chapters = total_chapters % num_days
    while start_date < end_date:
        if extra_chapters > 0:
            yield start_date, chapters_per_day + 1
            extra_chapters -= 1
        else:
            yield start_date, chapters_per_day
        start_date += timedelta(days=1)


def reading_plan(start_date: date, end_date: date, books: typing.List[Book]):
    all_chapters = chapters(books)
    total_chapters = sum(book.num_chapters for book in books)
    for plan_date, todays_chapters in chapter_counts_per_day(
        start_date, end_date, total_chapters
    ):
        for _ in range(todays_chapters):
            yield next(all_chapters), plan_date


@click.command()
@click.option("--start", prompt="What date will you start reading?")
@click.option("--next-alli-date", prompt="When is your next ALLI meeting?")
@click.option("--requested-books", prompt="Which books do you need to read?")
def calculate_reading_plan(start, next_alli_date, requested_books: str):
    try:
        start_date = dateparser.parse(start).date()
        end_date = dateparser.parse(next_alli_date).date()
    except AttributeError:
        print("Could not parse the start or end date.")
        sys.exit(1)

    books = [
        all_books[book.strip().capitalize()] for book in requested_books.split(",")
    ]
    pprint(list(reading_plan(start_date, end_date, books)))


if __name__ == "__main__":
    calculate_reading_plan()
