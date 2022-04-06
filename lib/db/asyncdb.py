import aiosqlite
import os

project_root = os.path.abspath(f"{os.curdir}")
name = os.path.abspath(f"{project_root}/res/karp.db")

test_root = "/home/jack/PycharmProjects/magikarpbot/res/karp.db"


async def increment_item_quantity(values):
    params = (values[0], values[1], values[2], values[0], values[1])
    try:
        db = await aiosqlite.connect(test_root)
        cursor = await db.cursor()
        sql = '''UPDATE inventory 
        SET quantity = (SELECT quantity FROM inventory WHERE trainerId = ? AND itemId = ?) + ? 
        WHERE trainerId = ? AND itemId = ?'''

        await cursor.execute(sql, params)
        await db.commit()
        await cursor.close()
        await db.close()
        return True
    except aiosqlite.OperationalError as err:
        print("[ERROR] Failed to write to inventory")
        return err


async def inventory_read(trainer_id):
    sql = '''SELECT items.itemName, inventory.quantity 
    FROM items INNER JOIN inventory ON items.itemId = inventory.itemId 
    WHERE inventory.trainerId = ?'''

    try:
        db = await aiosqlite.connect(test_root)
        cursor = await db.cursor()

        await cursor.execute(sql, (trainer_id,))
        data = await cursor.fetchall()

        await cursor.close()
        await db.close()

        return data

    except aiosqlite.OperationalError as err:
        print("[ERROR] Failed to read from inventory")
        return err


async def get_item_name_from_id(item_id):
    sql = "SELECT itemName FROM items WHERE itemId = ?"

    try:
        db = await aiosqlite.connect(test_root)
        cursor = await db.cursor()
        await cursor.execute(sql, (item_id,))
        data = await cursor.fetchone()
        await cursor.close()
        await db.close()
        if data[0] is None:
            return ""
        return data[0]
    except aiosqlite.OperationalError as err:
        print("[ERROR] Failed to read from items", err)
        return ""


async def get_max_item():
    sql = "SELECT MAX(itemId) FROM items"

    try:
        db = await aiosqlite.connect(test_root)
        cursor = await db.cursor()
        await cursor.execute(sql)
        data = await cursor.fetchone()
        await cursor.close()
        await db.close()

        if data[0] is None:
            return 0
        else:
            return data[0]
    except aiosqlite.OperationalError as err:
        print("[ERROR] Failed to read from db", err)
        return 0


async def add_inventory(values):
    sql = "INSERT INTO inventory (trainerId, itemId, quantity) VALUES (?, ?, ?)"

    try:
        db = await aiosqlite.connect(test_root)
        cursor = await db.cursor()
        await cursor.execute(sql, values)
        await db.commit()
        await cursor.close()
        await db.close()
        return True
    except aiosqlite.OperationalError as err:
        print("[ERROR] Failed to write to inventory")
        return err


async def edit_inventory(values):
    if type(values[2] != int):
        try:
            values = list(values)
            values[2] = int(values[2])
            values = tuple(values)
        except ValueError as err:
            return err
    sql = "SELECT inventoryId FROM inventory WHERE trainerId = ? AND itemId = ?"

    try:
        db = await aiosqlite.connect(test_root)
        cursor = await db.cursor()
        await cursor.execute(sql, (values[0], values[1]))
        data = await cursor.fetchall()
        data_len = 0
        # This has the potential to be quite slow. len() does not work due to it being a row iterable rather than a
        # standard iterable such as a tuple or a list
        # Suggestions welcome
        for _ in data:
            data_len += 1
        if data_len > 0:
            await increment_item_quantity(values)
        else:
            await add_inventory(values)
    except aiosqlite.OperationalError as err:
        print(err)
        return err

