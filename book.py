class Book:
    def __init__(self, title, author, release_year):
        self.title = title
        self.author = author
        self.release_year = release_year

    def show_info(self):
        return f"Titel: {self.title}, Författare: {self.author}, År: {self.release_year}"

books = [
    Book("Harry Potter och de vises sten", "J.K. Rowling", 1997),
    Book("Sagan om ringen", "J.R.R. Tolkien", 1954),
    Book("1984", "George Orwell", 1949),
    Book("Hobbit", "J.R.R. Tolkien", 1937),
    Book("Pestens tid", "Stephen King", 1978)
]