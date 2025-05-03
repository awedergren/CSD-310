# Amanda Wedergren
# April 24, 2025
# Module 8.2 Assignment

import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values

# Function to display film information based on selected items.
def show_films(cursor, title):
    cursor.execute('SELECT film_name as Name, film_director as Director, genre_name as Genre, '
                   'studio_name as "Studio Name" from film INNER JOIN genre ON film.genre_id=genre.genre_id '
                   'INNER JOIN studio ON film.studio_id=studio.studio_id')
    films = cursor.fetchall()
    print('\n -- {} --'.format(title))
    for film in films:
        print('Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n'.format(film[0], film[1], film[2], film[3]))

#using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """

    # connect to the movies database
    db = mysql.connector.connect(**config)

    # output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],config["database"]))

    input('\n\n  Press any key to continue...\n')

    # Create cursor
    cursor = db.cursor()

    show_films(cursor, 'DISPLAYING FILMS')

    # Insert new film into table and commit the changes.
    cursor.execute('''INSERT INTO film (film_id, film_name, film_releaseDate, film_runtime, film_director, genre_id, studio_id) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', ('4', 'Avatar', '2009', '161', 'James Cameron', '2', '1'))
    db.commit()

    show_films(cursor, 'DISPLAYING FILMS AFTER INSERT')

    # Update data for a film already in the table and commit the changes.
    cursor.execute('''UPDATE film SET genre_id = "1" WHERE film_id = "2"''')
    db.commit()

    show_films(cursor, 'DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror')

    # Delete film data from the table and commit the changes.
    cursor.execute('''DELETE FROM film WHERE film_name = "GLadiator"''')
    db.commit()

    show_films(cursor, 'DISPLAYING FILMS AFTER DELETE')

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    db.close()

