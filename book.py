class Book:
    def __init__(self, title, author, release_year):
        self.title = title
        self.author = author
        self.release_year = release_year

    def show_info(self):
        return f"Titel: {self.title}, Författare: {self.author}, År: {self.release_year}"

books = [
    Book("1984", "George Orwell", 1949),
    Book("The Hobbit", "J.R.R. Tolkien", 1937),
    Book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 1997),
    Book("The Hunger Games", "Suzanne Collins", 2008),
    Book("The Martian", "Andy Weir", 2011),
    Book("The Midnight Library", "Matt Haig", 2020),
    Book("Project Hail Mary", "Andy Weir", 2021),
    Book("Klara and the Sun", "Kazuo Ishiguro", 2021),
    Book("Fourth Wing", "Rebecca Yarros", 2023),
    Book("Iron Flame", "Rebecca Yarros", 2023),
    Book("Yellowface", "R.F. Kuang", 2023),
    Book("Intermezzo", "Sally Rooney", 2024)
]