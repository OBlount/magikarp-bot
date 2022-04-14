import os.path

from lib.db.database_maker import CreateDatabase


ROOT = os.path.abspath(f"{os.curdir}")
DB_PATH = os.path.abspath(f"{ROOT}/res/karp.db")

CreateDatabase.create_database()
