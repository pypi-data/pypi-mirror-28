from pyriver.db import db


def execute():
    starter = """{
       "metadata": {
            "name": "My River",
            "user": "ptbrodie",
            "interval": "hourly",
            "entry": "MyEntry.py"
       },
       "data": {
            "_comment": "your data here"
       }
    }"""
    with open("river.json", "w+") as schema:
        schema.writelines(starter)

    db.initdb()
    # TODO:initialize database (use sqlite for now)
