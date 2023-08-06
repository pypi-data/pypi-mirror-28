import imp
import json

from pyriver.engine.manager import River


def execute():
    with open("river.json", "rb") as riverfile:
        schema = json.load(riverfile)
        entry = schema.get("metadata", {}).get("entry")
        river = River()
        if entry:
            river = imp.load_source("river", entry).river
        river.init(schema)
        river.run()
