import sqlite3
import os
import random
from datetime import date
from book import Book, books

# Funktion för att rensa skärmen mellan olika menyer.
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def main():
    connection = sqlite3.connect("library.db")
    crsr = connection.cursor()

    sql_users = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    förnamn VARCHAR(40),
    efternamn VARCHAR(40),
    personnummer VARCHAR(40),
    ålder INTEGER);"""

    crsr.execute(sql_users)

    sql_books = """CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(40),
    author VARCHAR(40),
    release_year INTEGER);"""

    crsr.execute(sql_books)

    sql_loans = """CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    books_id INTEGER,
    loan_date VARCHAR(10),
    return_date VARCHAR(10),
    user_id INTEGER,
    FOREIGN KEY (books_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id));"""

    crsr.execute(sql_loans)

    for book in books:
        crsr.execute("SELECT * FROM books WHERE title = ?", (book.title,))
        existing_book = crsr.fetchone()

        if not existing_book:
                crsr.execute(
                    "INSERT INTO books (title, author, release_year) VALUES (?, ?, ?)",
                    (book.title, book.author, book.release_year)
                )

    connection.commit()

    while True:
        print("Välkommen till biblioteket!")

        print("\n1. Logga in.")
        print("2. Admin")
        print("3. Avsluta")

        try:
            menu = int(input("\nVad vill du göra? (1/2/3): "))

            if menu == 1:
                clear_screen()
                login(crsr, connection)
            elif menu == 2:
                clear_screen()
                admin(crsr, connection)
            elif menu == 3:
                break
            else:
                clear_screen()
                print("Ogiltigt val, försök igen.\n")

        except ValueError:
            clear_screen()
            print("Ogiltigt input, försök igen.\n")

def login(crsr, connection):
    choice = input("Har du ett konto? (J / N): ").lower()
    if choice == "j":
        clear_screen()
        print("---- Logga in ----")
        name = input("\nAnge ditt förnamn: ")
        last_name = input("Ange ditt efternamn: ")
        user = check_user(crsr, name, last_name)
        if user:
            while True:
                clear_screen()
                print(f"Välkommen tillbaka, {name.capitalize()}!\n")
                print("1. Låna en bok.")
                print("2. Lämna tillbaka en bok.")
                print("3. Logga ut.")
                try:
                    choice = int(input("\nVad vill du göra? (1/2/3): "))
                    if choice == 1:
                        clear_screen()
                        available_books = show_available_books(crsr)
                        borrow_book(crsr, connection, available_books, user[0])
                    elif choice == 2:
                        clear_screen()
                        borrowed_books = show_borrowed_books(crsr, user[0])
                        return_book(crsr, connection, borrowed_books)
                    elif choice == 3:
                        clear_screen()
                        return
                except ValueError:
                    print("Ogiltigt val. Försök igen")

        else:
            while True:
                choice = input("\nKontot hittades inte. Vill du skapa ett? (J / N): ").lower()
                if choice == "j":
                    clear_screen()
                    create_user(crsr, connection)
                    break
                elif choice == "n":
                    clear_screen()
                    break
                else:
                    print("Ogiltig input. Försök igen.")

    elif choice == "n":
        clear_screen()
        create_user(crsr, connection)
    else:
        clear_screen()
        print("Ogiltigt val. Försök igen.\n")

def admin(crsr, connection):
    while True:
        print("----- ADMIN -----")

        print("\n1. Visa alla användare.")
        print("2. Visa alla aktiva lån.")
        print("3. Tillbaka.")
        try:
            choice = int(input("\nVad vill du göra? (1/2/3): "))

            if choice == 1:
                clear_screen()
                show_users(crsr)
            elif choice ==2:
                clear_screen()
                show_all_loans(crsr)
            elif choice == 3:
                clear_screen()
                return
            else:
                print("Ogiltigt val. Försök igen")

        except ValueError:
            print("Ogiltig input. Försök igen.")

def create_user(crsr, connection):
    while True:
        print("----- Skapa ett konto -----")
        name = input("\nAnge ditt namn (eller 'Q' för att avsluta): ")
        if name.lower() == "q":
            print("\nAvslutar...")
            break

        last_name = input("Ange ditt efternamn: ")
        while True:
            birthdate = input("Ange ditt födelsedatum (ÅÅÅÅMMDD): ")
            if len(birthdate) != 8:
                print("\nOgiltigt födelsedatum, ange i formatet 'ÅÅÅÅMMDD'\n")
                continue

            try:
                year = int(birthdate[0:4])
                month = int(birthdate[4:6])
                day = int(birthdate[6:8])
                break
            except ValueError:
                print("Ogiltigt födelsedatum, använd endast siffror.")

        # Skapar ett förenklat personnummer med födelsedatum och fyra slumpade siffror
        last_four = str(random.randint(1000, 9999))
        personnumber = birthdate + "-" + last_four

        # Räknar ut personens nuvarande ålder och kontrollerar om födelsedagen har varit
        current_date = date.today()

        birthday_this_year = (month, day)
        today_month_day = (current_date.month, current_date.day)

        if today_month_day < birthday_this_year:
            age = current_date.year - year - 1
        else:
            age = current_date.year - year

        user = check_user(crsr, name, last_name)
        if user:
            print("\nAnvändaren finns redan.\n")
            while True:
                choice = input("Försök igen? (J / N): ").lower()
                if choice == "j":
                    clear_screen()
                    break
                elif choice == "n":
                    clear_screen()
                    return
        else:
            crsr.execute(
                "INSERT INTO users (förnamn, efternamn, personnummer, ålder) VALUES (?, ?, ?, ?)",
                (name, last_name, personnumber, age)
            )
            connection.commit()
            clear_screen()
            break

def check_user(crsr, name, last_name):
    crsr.execute("SELECT * FROM users WHERE LOWER(förnamn) = ? AND LOWER(efternamn) = ?",
                (name.lower(), last_name.lower())
    )
    result = crsr.fetchone()
    return result 

def show_available_books(crsr):
    crsr.execute("""
        SELECT * FROM books WHERE id NOT IN (
            SELECT books_id FROM loans WHERE return_date IS NULL
        )
    """)
    available_books = crsr.fetchall()

    print("\n----- Tillgängliga böcker -----")
    for book in available_books:
        print(f"Bok-ID: {book[0]} | {book[1]} av {book[2]}, {book[3]}")

    return available_books

def borrow_book(crsr, connection, available_books, user_id):
    if not available_books:
        print("\nInga tillgänglika böcker just nu.")
        input("\nTryck Enter för att fortsätta...")
        return
    while True:
        try:
            book_id = int(input("\nAnge bok-ID för boken du vill låna: "))
            break
        except ValueError:
            print("\nOgiltig input. Försök igen.")

    book_found = False
    for book in available_books:
        if book_id == book[0]:
            book_found = True
            book_title = book[1]

    if book_found:
        crsr.execute(
            "INSERT INTO loans (books_id, user_id, loan_date) VALUES (?, ?, ?)",
            (book_id, user_id, str(date.today()))
        )
        connection.commit()
        print(f"\n{book_title} har lånats!")
    else:
        print("\nOgiltigt bok-ID.")

    input("\nTryck Enter för att fortsätta...")

def show_borrowed_books(crsr, user_id):
    crsr.execute("""
        SELECT loans.id, books.id, books.title, books.author, books.release_year
        FROM loans
        JOIN books ON loans.books_id = books.id
        WHERE loans.user_id = ? AND return_date IS NULL    
    """, (user_id,))

    borrowed_books = crsr.fetchall()

    print("\n----- Lånade böcker -----")
    for book in borrowed_books:
        print(f"Lån-ID: {book[0]} | {book[2]} av {book[3]}, {book[4]}")

    return borrowed_books

def return_book(crsr, connection, borrowed_books):
    if not borrowed_books:
        print("\nDu har inte lånat några böcker.")
        input("\nTryck Enter för att fortsätta...")
        return

    while True:
        try:
            loan_id = int(input("\nAnge lån-ID för boken du vill lämna tillbaka: "))
            break
        except ValueError:
            print("\nOgiltig input. Försök igen.")

    loan_found = False
    for book in borrowed_books:
        if loan_id == book[0]:
            loan_found = True
            book_title = book[2]

    if loan_found:
        crsr.execute(
            "UPDATE loans SET return_date = ? WHERE id = ?",
            (str(date.today()), loan_id)
        )
        connection.commit()
        print(f"\n{book_title} har lämnats tillbaka!")
    else:
        print("\nOgiltigt lån-ID.")

    input("\nTryck Enter för att fortsätta...")

def show_users(crsr):
    crsr.execute("SELECT * FROM users")
    all_users = crsr.fetchall()

    print("----- Alla användare -----")

    if not all_users:
        print("\nDet finns inga användare.")
        input("\nTryck Enter för att fortsätta...")
        clear_screen()
        return

    for user in all_users:
        print(f"Namn: {user[1]}, Efternamn: {user[2]}, personnummer: {user[3]}, Ålder: {user[4]}")

    input("\nTryck Enter för att fortsätta...")
    clear_screen()
    return

def show_all_loans(crsr):
    crsr.execute("""
        SELECT users.förnamn, users.efternamn, books.title, books.author
        FROM loans
        JOIN users ON loans.user_id = users.id
        JOIN books ON loans.books_id = books.id
        WHERE loans.return_date IS NULL
    """)

    all_loans = crsr.fetchall()

    print("----- Alla aktiva lån -----")

    if not all_loans:
        print("\nDet finns inga aktiva lån.")
        input("\nTryck Enter för att fortsätta...")
        clear_screen()
        return
    
    for loan in all_loans:
        print(f"{loan[0]} {loan[1]} lånar {loan[2]} av {loan[3]} ")

    input("\nTryck Enter för att fortsätta...")
    clear_screen()
    return

if __name__ == "__main__":
    main()