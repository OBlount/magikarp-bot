import sqlite3
import os


class DatabaseManager:

    def __init__(self):
        self.project_root = f"{os.curdir}/../"
        self.name = f"{os.curdir}/../res/karp.db"
        self.create_db()
        self.connection = None
        self.cursor = None
        self.establish_connection()

    def create_db(self):
        if not os.path.isfile(self.name):
            os.mkdir(f"{self.project_root}/res")

    def establish_connection(self):  # connects to db and creates cursor
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            print("[INFO] Established Connection with the database")
        except sqlite3.DatabaseError:
            print("[ERROR] Failed to establish connection with the database")
            exit()

    def close_connection(self):  # closes connection
        self.connection.close()


class DbAdminCommands(DatabaseManager):

    def __init__(self):
        super().__init__()

    # Adds new item to the items table in the db.
    # DOCUMENTATION:
    # tuple params = (itemType, itemName, itemDesc, itemEffect)
    def db_add_new_item(self, params):
        params = tuple(params)
        try:
            sql = "INSERT INTO items (itemType, itemName, itemDesc, itemEffect) VALUES (?, ?, ?, ?)"
            self.cursor.execute(sql, params)
            self.connection.commit()
            print("[SUCCESS] Written to items successfully")
            return True
        except sqlite3.OperationalError:
            print("[ERROR] Failed to write to items")
            return False

    # Adds new trainer to the trainer table in the db.
    # DOCUMENTATION:
    # trainerId = Discord ID
    # trainerName = Discord Name
    # tuple values = (trainerId, trainerName)
    def db_add_trainer(self, values):
        params = tuple(values)
        sql = "INSERT INTO trainers (trainerId, trainerName) VALUES (?, ?)"
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            print("[SUCCESS] Written to trainers successfully")
            return True
        except sqlite3.OperationalError:
            print("[ERROR] Failed to write to trainers")
            return False




if __name__ == '__main__':
    pass
