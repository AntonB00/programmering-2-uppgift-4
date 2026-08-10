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
        choice = input("Har du ett konto? (J / N): ").lower()
        if choice == "j":
            clear_screen()
            print("---- Logga in ----")
            name = input("\nAnge ditt förnamn: ")
            last_name = input("Ange ditt efternamn: ")
            user = check_user(crsr, name, last_name)
            if user:
                print(f"Välkommen tillbaka, {name.capitalize()}!\n")
            else:
                while True:
                    choice = input("\nKontot hittades inte. Vill du skapa ett? (J / N): ").lower()
                    if choice == "j":
                        clear_screen()
                        create_user(crsr, connection)
                    elif choice == "n":
                        clear_screen()
                        break
                    else:
                        print("Ogiltig input. Försök igen.")

        elif choice == "n":
            clear_screen()
            create_user(crsr, connection)

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
                print("Ogiltigt födelsedatum, ange i formatet 'ÅÅÅÅMMDD'")
            else:
                break

        # Skapar ett förenklat personnummer med födelsedatum och fyra slumpade siffror
        last_four = str(random.randint(1000, 9999))
        personnumber = birthdate + "-" + last_four

        # Räknar ut personens nuvarande ålder och kontrollerar om födelsedagen har varit
        current_date = date.today()

        year = int(birthdate[0:4])
        month = int(birthdate[4:6])
        day = int(birthdate[6:8])

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
                    main()
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



if __name__ == "__main__":
    main()