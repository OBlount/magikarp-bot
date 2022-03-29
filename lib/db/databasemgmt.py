import sqlite3
import os


class DatabaseManager:

    def __init__(self):
        self.project_root = os.path.abspath(f"{os.curdir}")
        self.name = os.path.abspath(f"{self.project_root}/res/karp.db")
        self.connection = None
        self.cursor = None
        self.establish_connection()

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
    # tuple params = (int itemType, string itemName, string itemDesc, int itemEffect)
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
    # tuple values = (int trainerId, string trainerName)
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

    # Method to change the number of items of a specified trainer.
    # DOCUMENTATION:
    # tuple values = (trainerId, itemId, quantity)
    # Note: Quantity should be the new quantity not the amount to add/remove.
    # E.g. Current quantity is 25 and 5 items should be added, the new quantity should = 30.
    def update_inventory(self, values):
        params = [values[2], values[0], values[1]]
        sql = "UPDATE inventory SET quantity = ? WHERE trainerId = ? AND itemId = ?"
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            print("[SUCCESS] Written to inventory successfully")
            return True
        except sqlite3.OperationalError as err:
            print("[ERROR] Failed to write to inventory")
            return err


class DbOperations(DatabaseManager):

    def __init__(self):
        super().__init__()

    # A private method to increment a trainer's quantity of an item.
    # DOCUMENTATION:
    # tuple values = (int trainerId, int itemId, int quantity)
    def __increment_item_quantity(self, values):
        params = (values[0], values[1], values[2], values[0], values[1])
        try:
            sql = '''UPDATE inventory 
            SET quantity = (SELECT quantity FROM inventory WHERE trainerId = ? AND itemId = ?) + ? 
            WHERE trainerId = ? AND itemId = ?'''
            self.cursor.execute(sql, params)
            self.connection.commit()
            print("[SUCCESS] Written to inventory successfully")
            return True
        except sqlite3.OperationalError as err:
            print("[ERROR] Failed to write to inventory")
            return err

    # A private method to decrement a trainer's quantity of an item.
    # DOCUMENTATION:
    # tuple values = (int trainerId, int itemId, int quantity)
    def __decrement_item_quantity(self, values):
        params = (values[0], values[1], values[2], values[0], values[1])
        try:
            sql = '''UPDATE inventory 
            SET quantity = (SELECT quantity FROM inventory WHERE trainerId = ? AND itemId = ?) - ? 
            WHERE trainerId = ? AND itemId = ?'''
            self.cursor.execute(sql, params)
            self.connection.commit()
            print("[SUCCESS] Written to inventory successfully")
            return True
        except sqlite3.OperationalError as err:
            print("[ERROR] Failed to write to inventory")
            return err

    # A private method to get the item id of an item from the name of an item.
    # DOCUMENTATION:
    # string item_name
    # RETURNS:
    # int item_id
    def __get_item_from_name(self, item_name):
        item_name = item_name.lower()
        sql = "SELECT itemId FROM items WHERE LOWER(itemName) =:itemName"

        self.cursor.execute(sql, {"itemName": item_name})
        data = self.cursor.fetchall()
        return data

    # A private method to get the trainer id from a trainer's name
    # DOCUMENTATION:
    # string trainer_name
    # RETURNS:
    # int trainer_id
    def __get_trainer_id_from_name(self, trainer_name):
        trainer_name = trainer_name.lower()
        sql = "SELECT trainerId FROM trainers WHERE LOWER(trainerName) =:trainerName"

        self.cursor.execute(sql, {"trainerName": trainer_name})
        data = self.cursor.fetchall()
        return data

    # A method to read the inventory of a specified trainer by passing the id
    # DOCUMENTATION:
    # int trainer_id
    # RETURNS:
    # array [(item1_name, item1_quantity), (item2_id, item2_quantity), ... ]
    def inventory_read(self, trainer_id):
        sql = '''SELECT items.itemName, inventory.quantity 
        FROM items INNER JOIN inventory ON items.itemId = inventory.itemId 
        WHERE inventory.trainerId =:trainerID'''

        self.cursor.execute(sql, {"trainerID": trainer_id})
        data = self.cursor.fetchall()
        return data

    # A private method that adds a new item to a trainer's inventory.
    # DOCUMENTATION:
    # tuple values = (int trainerId, int itemId, int quantity)
    def __add_inventory(self, values):
        params = tuple(values)
        sql = "INSERT INTO inventory (trainerId, itemId, quantity) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            print("[SUCCESS] Written to inventory successfully")
            return True
        except sqlite3.OperationalError as err:
            print("[ERROR] Failed to write to inventory")
            return err

    # An important method when editing a trainer's inventory. It will add_inventory() or increment_item_quantity()
    # depending on if the item is already in the trainer's inventory.
    # DOCUMENTATION:
    # tuple values = (any trainerId, any itemId, any quantity)
    # Note: The function is smart so that you can pass in string names.
    def edit_inventory(self, values):
        if type(values[0]) != int:
            values[0] = self.__get_trainer_id_from_name(values[0])[0][0]
        if type(values[1]) != int:
            values[1] = self.get_item_from_name(values[1])[0][0]
        if type(values[2]) != int:
            try:
                values = list(values)
                values[2] = int(values[2])
                values = tuple(values)
            except ValueError as err:
                return err
        sql = "SELECT inventoryId FROM inventory WHERE trainerId = ? AND itemId = ?"
        try:
            self.cursor.execute(sql, (values[0], values[1]))
            data = self.cursor.fetchall()
            if len(data) > 0:
                self.increment_item_quantity(values)
            else:
                self.add_inventory(values)
        except sqlite3.OperationalError as err:
            print(err)
            return err

    # Method that gets the amount of items in the db.
    # DOCUMENTATION:
    # RETURNS:
    # int number_of_items
    def get_max_item(self):
        sql = "SELECT MAX(itemId) FROM items"
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return int(data[0])

    # Method that gets the item's name in the db.
    # DOCUMENTATION:
    # int item_id
    # RETURNS:
    # string item_name
    def get_item_name_from_id(self, item_id):
        sql = "SELECT itemName FROM items WHERE itemId = ?"
        self.cursor.execute(sql, (item_id,))
        data = self.cursor.fetchone()
        return data[0]


if __name__ == '__main__':
    pass
