import random
from datetime import date

if __name__ == "__main__":
    while True:
        name = input("Ange ditt namn (eller 'Q' för att avsluta): ")
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

        print(f"Namn: {name} {last_name}")
        print(f"Personnummer: {personnumber}")
        print(f"Ålder: {age}")