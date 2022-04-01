import os.path
import sqlite3


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
                exit()
        else:
            pass

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


if __name__ == '__main__':
    pass
