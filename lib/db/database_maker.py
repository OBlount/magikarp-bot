import os.path
import sqlite3

from lib.db import __DB_PATH, __DIR
from lib.db.pokemon_grabber import *


# A method to create the database file. It will also
# automatically create the tables needed for a fresh new game
# (as well as add the starting items, itemTypes, ect...).
# If the database file exists, then is will validate the
# tables.
def create_database():
    if not __check_if_db_exists():
        print("[DB] Database cannot be found\n[DB] Creating new database")
        os.mkdir(__DIR)
        print("[DB] Made dir res/")
        try:
            connection = sqlite3.connect(__DB_PATH)
            cursor = connection.cursor()
            CreateTableSQL.create_tables(cursor, connection)
            connection.close()
            print("[DB] Done")
        except sqlite3.DatabaseError:
            print("[ERROR] Trouble creating the database")
            __clean_database(cursor, connection)
            exit()
    else:
        try:
            connection = sqlite3.connect(__DB_PATH)
            cursor = connection.cursor()

            if not is_species_table_valid(cursor, connection):
                print("[ERROR] Trouble validating the table 'pokemonspecies'")
                __clean_database(cursor, connection, ["pokemonspecies"])
                CreateTableSQL.insert_pokemon_species(cursor, connection)
                print("[DB] Exiting. Please restart the bot...")
                exit()

            connection.close()
            print("[DB] Done")
        except sqlite3.DatabaseError:
            print("[ERROR] Trouble validating the database")
            exit()

# A method that checks and returns True if
# the species table exists. Note that if the table
# exists but it's invalid, then the table is dumped.
# DOCUMENTATION:
# cursor cursor
# connection connection
# RETURNS:
# boolean is_valid
def is_species_table_valid(cursor, connection):
    sql_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='pokemonspecies'"
    sql_valid = "SELECT * FROM pokemonspecies"
    sql_remove = "DELETE FROM pokemonspecies"
    cursor.execute(sql_exists)
    connection.commit()
    data = cursor.fetchall()

    if len(data) <= 0:
        return False

    cursor.execute(sql_valid)
    connection.commit()
    data = cursor.fetchall()

    if len(data) != 151:
        cursor.execute(sql_remove)
        connection.commit()
        return False
    return True


# A method that constructs a string, consisting
# off all pokemon, that fits inside the
# VALUES part of the SQL statement. E.g. the string
# will look like: (0, "pokemon", ...), (...), (...).
# This is needed to create/format the sql statement which
# populates the pokemonspecies table.
# DOCUMENTATION:
# RETURNS:
# string values
def format_sql_values_for_species():
    values = ""
    number_of_pokemon = get_pokemon_species_count()

    # If we return an empty "", we break the sql statement
    if not number_of_pokemon or number_of_pokemon != 151:
        return ""

    print("[API] Grabbing pokemon...")
    for pokemon_id in range(number_of_pokemon):
        pokemon_attributes = get_a_pokemons_attributes(pokemon_id + 1)

        if not pokemon_attributes:
            return ""

        # Deconstruct the dictionary
        pokedex = pokemon_attributes["pokedex_ID"]
        name = pokemon_attributes["name"]
        evolves_from = pokemon_attributes["evolves_from"]

        # Each iteration of the for loop, we begin our 'record' as follows
        record = "(" + str(pokedex) + ", "  + f'"{name}"' + ", "

        # Here we need some logic to check if we need to put NULL or not in this specific field
        if evolves_from == None:
            record = record + "NULL"
        else:
            evolution_species_ID = get_pokedexID_from_name(evolves_from["name"])
            record = record + str(evolution_species_ID)

        # When we have reached the pokemonID 150 (+1), structure the string without the ',\n\r'
        if not pokemon_id + 1 == number_of_pokemon:
            record = record + "),\n\r"
        else:
            record = record + ")"

        # We add this completed 'record' to the values string
        values = values + record
    return values

# A private method to check if the db file exists.
# DOCUMENTATION:
# RETURNS:
# boolean exists
def __check_if_db_exists():
    return os.path.exists(__DB_PATH)


# A private method that removes tables. It can also
# remove the enire (this includes the file.db and the dir/).
# DOCUMENTATION:
# list(strings) tables
def __clean_database(cursor, connection, tables=None):
    if not __check_if_db_exists():
        return

    if tables == None:
        print("[DB] Removing " + __DB_PATH + "/")
        os.remove(__DB_PATH)
        os.rmdir(__DIR)
    elif len(tables) <= 0:
        return
    else:
        for table in tables:
            sql = "DELETE FROM " + table
            print(f"[DB] Cleaning table '{table}'")
            cursor.execute(sql)
            connection.commit()


class CreateTableSQL():

    __tbl_trainers = '''
        CREATE TABLE trainers (
        trainerID INTEGER PRIMARY KEY,
        trainerName TEXT
    )'''

    __tbl_itemtypes = '''
        CREATE TABLE "itemtypes" (
        "typeId"    INTEGER,
        "typeDesc"  TEXT NOT NULL,
        PRIMARY KEY("typeId")
    )'''

    __tbl_add_itemtypes = '''
        INSERT INTO itemtypes (typeId, typeDesc)
        VALUES (1, "Healing")
    '''

    __tbl_items = '''
        CREATE TABLE "items" (
        "itemId"    INTEGER,
        "itemType"  INTEGER,
        "itemName"  TEXT NOT NULL,
        "itemDesc"  TEXT NOT NULL,
        "itemEffect"    INTEGER,
        PRIMARY KEY("itemId" AUTOINCREMENT),
        FOREIGN KEY("itemType") REFERENCES "itemtypes"("typeId") ON DELETE CASCADE
    )'''

    __tbl_add_items = '''
        INSERT INTO items (itemId, itemType, itemName, itemDesc, itemEffect)
        VALUES
            (1, 1, "Potion", "Restores HP that have been lost in battle by 20 HP.", 20),
            (2, 1, "Super Potion", "Restores HP that have been lost in battle by 50 HP.", 50)
    '''

    __tbl_inventory = '''
        CREATE TABLE "inventory" (
        "inventoryId"   INTEGER,
        "itemId"    INTEGER,
        "trainerId" INTEGER,
        "quantity"  INTEGER,
        PRIMARY KEY("inventoryId"),
        FOREIGN KEY("trainerId") REFERENCES "trainers"("trainerID") ON DELETE CASCADE,
        FOREIGN KEY("itemId") REFERENCES "items"("itemId") ON DELETE CASCADE
    )'''

    __tbl_pokemon_species = '''
        CREATE TABLE "pokemonspecies" (
        "pokedexNumber" INTEGER NOT NULL,
        "name"          TEXT NOT NULL,
        "evolvesFromID" INTEGER,
        PRIMARY KEY("pokedexNumber")
    )'''

    # A static method that grabs the pokemon species from
    # the API, and then inserts them into the table. This is used
    # When creating the database, and when the table isn't valid.
    # DOCUMENTATION:
    # cursor cursor
    # connection connection
    @staticmethod
    def insert_pokemon_species(cursor, connection):
        add_species_statement = f'''
        {"INSERT INTO pokemonspecies (pokedexNumber, name, evolvesFromID) VALUES " if not is_species_table_valid(cursor, connection) else ""}
            {format_sql_values_for_species() if not is_species_table_valid(cursor, connection) else ""}
        '''
        cursor.execute(add_species_statement)
        connection.commit()

    # A static method that commits all the sql passed into
    # the function (to create the tables).
    # DOCUMENTATION:
    # cursor cursor
    # connection connection
    @staticmethod
    def create_tables(cursor, connection):
        sql_statements = CreateTableSQL.__get_all_table_statements()
        for statement in sql_statements:
            cursor.execute(statement)
            connection.commit()
        # Special case for dynamic SQL statement - add species.
        CreateTableSQL.insert_pokemon_species(cursor, connection)

    # A private static method to get all the sql
    # statements (above), returned as a list(strings).
    # DOCUMENTATION:
    # RETURNS:
    # list(strings) statements
    @staticmethod
    def __get_all_table_statements():
        statements = []
        for var in CreateTableSQL.__dict__:
            if var[:21] == "_CreateTableSQL__tbl_":
                statements.append(getattr(CreateTableSQL, var))
        return statements


if __name__ == '__main__':
    pass
