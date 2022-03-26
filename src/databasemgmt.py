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


class DbRead(DatabaseManager):

    def __init__(self):
        super().__init__()

    def debug(self):
        sql = "SELECT * FROM trainers;"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print(data)

    def read(self, table, select_params, where_clause="1=1"):
        params = ', '.join([param for param in select_params])
        sql = f"SELECT {params} FROM {table} WHERE {where_clause}"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def inventory_read(self, trainer_id):
        sql = '''SELECT items.itemName, inventory.quantity 
        FROM items INNER JOIN inventory ON items.itemId = inventory.itemId 
        WHERE inventory.trainerId =:trainerID'''

        self.cursor.execute(sql, {"trainerID": trainer_id})
        data = self.cursor.fetchall()
        return data


class DbWrite(DatabaseManager):

    def __init__(self):
        super().__init__()

    def db_add_inventory(self, values):
        params = tuple(values)
        sql = "INSERT INTO inventory (itemId, trainerId, quantity) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            print("[SUCCESS] Written to inventory successfully")
            return True
        except sqlite3.OperationalError:
            print("[ERROR] Failed to write to inventory")
            return False

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
