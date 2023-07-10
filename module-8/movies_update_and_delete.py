import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "movies_user",
    "password": "popcorn",
    "host": "127.0.0.1",
    "port": "7070",
    "database": "movies",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    
    print("\n Database User {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    input("\n\n Press enter to continue...")

    cursor = db.cursor()

    def show_films(cursor, title):
        cursor.execute("SELECT film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' FROM film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id")
        films = cursor.fetchall()
        print("\n -- {} --".format(title))
        
        for film in films:
            print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0],film[1],film[2],film[3]))


    show_films(cursor, "DISPLAYING FILMS")

    cursor.execute("INSERT INTO film (film_name, film_director, genre_id, studio_id, film_releaseDate, film_runtime) VALUES ('Jurassic World', 'Colin Trevorrow', 1, 3, 2015, 124)")

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    cursor.execute("UPDATE film SET genre_id = 1 WHERE film_name = 'Alien'")

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator'")

    show_films(cursor, "DISPLAYING FILMS AFTER DELETION")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The specified username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)
finally:
    if db.is_connected():
        cursor.close()
        db.close()
        print("\n MySQL connection closed.")