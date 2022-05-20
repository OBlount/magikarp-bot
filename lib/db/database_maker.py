import os.path
import sqlite3

from lib.db.pokemon_grabber import *


class CreateDatabase():

    __PATH = os.path.abspath(f"{os.curdir}/res/karp.db")
    __DIR = "res"

    # A private static method to check if the db file exists.
    # DOCUMENTATION:
    # RETURNS:
    # boolean exists
    @staticmethod
    def __check_if_db_exists():
        return os.path.exists(CreateDatabase.__PATH)


    # A static method to create the database file. It will also
    # automatically create the tables needed for a fresh new game
    # (as well as add the starting items, itemTypes, ect...).
    # If the database file exists, then is will validate the
    # tables.
    @staticmethod
    def create_database():
        if not CreateDatabase.__check_if_db_exists():
            print("[DB] Database cannot be found\n[DB] Creating new database")
            os.mkdir(CreateDatabase.__DIR)
            print("[DB] Made dir res/")
            try:
                connection = sqlite3.connect(CreateDatabase.__PATH)
                cursor = connection.cursor()
                CreateTableSQL.create_tables(cursor, connection)
                connection.close()
                print("[DB] Done")
            except sqlite3.DatabaseError:
                print("[ERROR] Trouble creating the database")
                CreateDatabase.__clean_database()
                exit()
        else:
            try:
                connection = sqlite3.connect(CreateDatabase.__PATH)
                cursor = connection.cursor()

                if not CreateDatabase.is_species_table_valid(cursor, connection):
                    print("[ERROR] Trouble validating the database")
                    CreateDatabase.__clean_database()
                    exit()

                connection.close()
                print("[DB] Done")
            except sqlite3.DatabaseError:
                print("[ERROR] Trouble validating the database")
                exit()

    # A private static method that removes the enire database.
    # This includes the file.db and the dir/.
    def __clean_database():
        if CreateDatabase.__check_if_db_exists():
            print("[DB] Removing " + CreateDatabase.__PATH + "/")
            os.remove(CreateDatabase.__PATH)
            os.rmdir(CreateDatabase.__DIR)

    # A static method that checks and returns True if
    # the species table exists. Note that if the table
    # exists but it's invalid, then the table is dumped.
    # DOCUMENTATION:
    # cursor cursor
    # connection connection
    # RETURNS:
    # boolean is_valid
    @staticmethod
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


    # A static method that constructs a string,
    # consisting off all pokemon, that fits inside the
    # VALUES part of the SQL statement. E.g. the string
    # will look like: (0, "pokemon", ...), (...), (...).
    # This is needed to create/format the sql statement which
    # populates the pokemonspecies table.
    # DOCUMENTATION:
    # RETURNS:
    # string values
    @staticmethod
    def format_sql_values_for_species():
        values = ""
        number_of_pokemon = get_pokemon_species_count()

        # If we return an empty "", we break the sql statement
        if not number_of_pokemon or number_of_pokemon != 151:
            return ""

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
        add_species_statement = f'''
        {"INSERT INTO pokemonspecies (pokedexNumber, name, evolvesFromID) VALUES " if not CreateDatabase.is_species_table_valid(cursor, connection) else ""}
            {CreateDatabase.format_sql_values_for_species() if not CreateDatabase.is_species_table_valid(cursor, connection) else ""}
        '''
        cursor.execute(add_species_statement)
        connection.commit()


if __name__ == '__main__':
    pass
