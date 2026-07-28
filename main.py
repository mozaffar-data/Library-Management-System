import json
import random
import string
from pathlib import Path
from datetime import datetime


class Library:
    database = "library.json"
    data = {
        "books": [],
        "members": []
    }

    # Load existing data from JSON file
    # If file doesn't exist, create a new JSON file
    if Path(database).exists():
        try:
            with open(database, "r") as f:
                content = f.read().strip()

                if content:
                    data = json.loads(content)

        except (json.JSONDecodeError, FileNotFoundError):
            data = {
                "books": [],
                "members": []
            }

    else:
        with open(database, "w") as f:
            json.dump(data, f, indent=4)


    # Generate unique ID
    @staticmethod
    def gen_id(prefix="B"):
        random_id = ""

        for i in range(5):
            random_id += random.choice(
                string.ascii_uppercase + string.digits
            )

        return prefix + "-" + random_id


    # Save data to JSON file
    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as f:
            json.dump(
                cls.data,
                f,
                indent=4,
                default=str
            )


    # Add a new book
    def add_book(self):
        title = input("Give the title of your book :- ")
        author = input("Enter the name of the author :- ")
        copies = int(input("Enter the number of copies :- "))

        book = {
            "Book_id": Library.gen_id(),
            "Title": title,
            "Author_name": author,
            "Total_copies": copies,
            "Available_copies": copies,
            "added_on": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        Library.data["books"].append(book)

        Library.save_data()

        print("Book Added Successfully!")


    # List all books
    def list_book(self):
        if not Library.data["books"]:
            print("Sorry, no books found!")
            return

        print("\nBook ID      Title                     Author              Copies")
        print("-" * 75)

        for b in Library.data["books"]:
            print(
                f"{b['Book_id']:12}"
                f"{b['Title'][:24]:25}"
                f"{b['Author_name'][:19]:20}"
                f"{b['Total_copies']}/{b['Available_copies']}"
            )

        print()


    # Add a new member
    def add_member(self):
        name = input("Enter the name :- ")
        email = input("Enter your email :- ")

        member = {
            "id": Library.gen_id("M"),
            "name": name,
            "email": email,
            "borrowed": []
        }

        Library.data["members"].append(member)

        Library.save_data()

        print("Member Added Successfully!")


    # List all members
    def list_member(self):
        if not Library.data["members"]:
            print("Sorry, no members found!")
            return

        print("\nMember ID    Name                     Email")
        print("-" * 70)

        for m in Library.data["members"]:
            print(
                f"{m['id']:12}"
                f"{m['name'][:24]:25}"
                f"{m['email'][:29]:30}"
            )

            print("Borrowed Books:")

            if m["borrowed"]:
                for book in m["borrowed"]:
                    print(
                        f"  - {book['Title']} "
                        f"({book['book_id']})"
                    )
            else:
                print("  No borrowed books")

            print()


    # Borrow a book
    def borrow(self):
        member_id = input(
            "Enter the member ID :- "
        ).strip()

        members = [
            m for m in Library.data["members"]
            if m["id"] == member_id
        ]

        if not members:
            print("No such member exists!")
            return

        member = members[0]

        book_id = input(
            "Enter the book ID :- "
        ).strip()

        books = [
            b for b in Library.data["books"]
            if b["Book_id"] == book_id
        ]

        if not books:
            print("Sorry, no such book exists!")
            return

        book = books[0]

        if book["Available_copies"] <= 0:
            print("Sorry, no books available!")
            return

        borrow_entry = {
            "book_id": book["Book_id"],
            "Title": book["Title"],
            "Borrow_on": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        member["borrowed"].append(borrow_entry)

        book["Available_copies"] -= 1

        Library.save_data()

        print("Book Borrowed Successfully!")


    # Return a borrowed book
    def return_book(self):
        member_id = input(
            "Enter the member ID :- "
        ).strip()

        members = [
            m for m in Library.data["members"]
            if m["id"] == member_id
        ]

        if not members:
            print("No such member exists!")
            return

        member = members[0]

        if not member["borrowed"]:
            print("No borrowed books!")
            return

        print("\nBorrowed Books:")

        for i, b in enumerate(
            member["borrowed"],
            start=1
        ):
            print(
                f"{i}. {b['Title']} "
                f"({b['book_id']})"
            )

        try:
            choice = int(
                input(
                    "Enter number to return :- "
                )
            )

            if choice < 1 or choice > len(
                member["borrowed"]
            ):
                print("Invalid book number!")
                return

            selected = member["borrowed"].pop(
                choice - 1
            )

        except ValueError:
            print("Invalid value!")
            return

        books = [
            bk for bk in Library.data["books"]
            if bk["Book_id"] == selected["book_id"]
        ]

        if books:
            books[0]["Available_copies"] += 1

        Library.save_data()

        print("Book Returned Successfully!")


# --------------------------------------------------
# CONSOLE PROGRAM
# This section will only run when you directly run:
# python main.py
#
# It will NOT run when Streamlit imports Library
# using:
# from main import Library
# --------------------------------------------------

if __name__ == "__main__":

    hello = Library()

    while True:

        print("=" * 50)
        print("Library Management System")
        print("1. Add Book")
        print("2. List Books")
        print("3. Add Members")
        print("4. List Members")
        print("5. Borrow Books")
        print("6. Return Books")
        print("0. Exit the Portal")
        print("-" * 50)

        choice = input(
            "What task you want to perform :- "
        )

        if choice == "1":
            hello.add_book()

        elif choice == "2":
            hello.list_book()

        elif choice == "3":
            hello.add_member()

        elif choice == "4":
            hello.list_member()

        elif choice == "5":
            hello.borrow()

        elif choice == "6":
            hello.return_book()

        elif choice == "0":
            print("Thank you for using Library Management System!")
            break

        else:
            print("Invalid choice! Please try again.")