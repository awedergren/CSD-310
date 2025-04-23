# Amanda Wedergren
# April 17, 2025
# Module 6.2 Assignment

import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": 'movies_user',
    "password": 'popcorn',
    "host": 'localhost',
    "database": 'movies',
    "raise_on_warnings": True #not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database

    # output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],config["database"]))

    input('\n\n  Press any key to continue...\n')

    # Query for the studio records
    cursor = db.cursor()
    cursor.execute('SELECT studio_id, studio_name FROM studio')
    studios = cursor.fetchall()
    print('-- DISPLAYING Studio RECORDS --')
    for studio in studios:
        print('Studio ID: {}\nStudio Name: {}\n'.format(studio[0], studio[1]))

    # Query for the genre records
    cursor = db.cursor()
    cursor.execute('SELECT genre_id, genre_name FROM genre')
    genres = cursor.fetchall()
    print('\n-- DISPLAYING Genre RECORDS --')
    for genre in genres:
        print('Genre ID: {}\nGenre Name: {}\n'.format(genre[0], genre[1]))

    # Query for the short film records. Show films that are less than 120 minutes long.
    cursor = db.cursor()
    cursor.execute('SELECT film_name, film_runtime FROM film WHERE film_runtime < 120')
    films = cursor.fetchall()
    print('\n-- DISPLAYING Short Film RECORDS --')
    for film in films:
        print('Film Name: {}\nRuntime: {}\n'.format(film[0], film[1]))

    # Query for the director records in order of movie release date (newest first)
    cursor = db.cursor()
    cursor.execute('SELECT film_name, film_director FROM film ORDER by film_releaseDate')
    films = cursor.fetchall()
    reversed_order = films[::-1]
    print('\n-- DISPLAYING Director RECORDS in Order --')
    for film in reversed_order:
        print('Film Name: {}\nDirector: {}\n'.format(film[0], film[1]))

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

