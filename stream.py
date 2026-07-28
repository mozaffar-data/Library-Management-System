import streamlit as st
from main import Library   # your existing file

lib = Library()

st.set_page_config(page_title="Library Management", layout="wide")

st.title("📚 Library Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Add Book",
        "List Books",
        "Add Member",
        "List Members",
        "Borrow Book",
        "Return Book"
    ]
)

# ---------------- ADD BOOK ----------------
if menu == "Add Book":
    st.header("Add Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    copies = st.number_input("Copies", min_value=1)

    if st.button("Add Book"):
        book = {
            "Book_id": Library.gen_id(),
            "Title": title,
            "Author_name": author,
            "Total_copies": copies,
            "Available_copies": copies
        }

        Library.data["books"].append(book)
        Library.save_data()

        st.success("Book Added Successfully")


# ---------------- LIST BOOKS ----------------
elif menu == "List Books":
    st.header("Books")

    books = Library.data["books"]

    if not books:
        st.warning("No books found")
    else:
        st.dataframe(books)


# ---------------- ADD MEMBER ----------------
elif menu == "Add Member":
    st.header("Add Member")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Add Member"):
        member = {
            "id": Library.gen_id("M"),
            "name": name,
            "email": email,
            "borrowed": []
        }

        Library.data["members"].append(member)
        Library.save_data()

        st.success("Member Added")


# ---------------- LIST MEMBERS ----------------
elif menu == "List Members":
    st.header("Members")

    members = Library.data["members"]

    if not members:
        st.warning("No members")
    else:
        st.dataframe(members)


# ---------------- BORROW BOOK ----------------
elif menu == "Borrow Book":
    st.header("Borrow Book")

    members = Library.data["members"]
    books = Library.data["books"]

    member_ids = [m["id"] for m in members]
    book_ids = [b["Book_id"] for b in books]

    member_id = st.selectbox("Select Member", member_ids)
    book_id = st.selectbox("Select Book", book_ids)

    if st.button("Borrow"):
        member = next(m for m in members if m["id"] == member_id)
        book = next(b for b in books if b["Book_id"] == book_id)

        if book["Available_copies"] <= 0:
            st.error("No copies available")
        else:
            borrow_entry = {
                "book_id": book["Book_id"],
                "Title": book["Title"]
            }

            member["borrowed"].append(borrow_entry)
            book["Available_copies"] -= 1

            Library.save_data()
            st.success("Book Borrowed")


# ---------------- RETURN BOOK ----------------
elif menu == "Return Book":
    st.header("Return Book")

    members = Library.data["members"]

    member_ids = [m["id"] for m in members]
    member_id = st.selectbox("Select Member", member_ids)

    member = next(m for m in members if m["id"] == member_id)

    borrowed = member["borrowed"]

    if not borrowed:
        st.warning("No borrowed books")

    else:
        book_titles = [
            f"{b['Title']} ({b['book_id']})"
            for b in borrowed
        ]

        selected = st.selectbox("Select Book", book_titles)

        if st.button("Return Book"):
            index = book_titles.index(selected)
            returned = member["borrowed"].pop(index)

            books = Library.data["books"]
            book = next(
                b for b in books
                if b["Book_id"] == returned["book_id"]
            )

            book["Available_copies"] += 1

            Library.save_data()
            st.success("Book Returned")