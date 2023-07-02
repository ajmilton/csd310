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
    cursor.execute ("SELECT * FROM studio")
    studios = cursor.fetchall()
    cursor.execute ("SELECT * FROM genre")
    genres = cursor.fetchall()
    cursor.execute ("SELECT film_name FROM film WHERE film_runtime <'%s'",[120])
    short_film = cursor.fetchall()
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    director = cursor.fetchall()

    RecordValue = ["Studios", "genres", "Short Films", "Director"]
    for i, query in enumerate([studios, genres, short_film, director]):
        print("\n -- DISPLAYING {} RECORDS{} --".format(RecordValue[i], " in Order" if i==3 else ""))

        column_widths = [max(len(str(col)) for col in row) for row in query]


        for row in query:
            formatted_row = [str(col).ljust(width) for col, width in zip(row, column_widths)]
            print(" | ".join(formatted_row))



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