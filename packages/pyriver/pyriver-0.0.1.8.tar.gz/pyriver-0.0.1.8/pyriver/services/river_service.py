import json

from pyriver.db import db
from pyriver.models import River, Channel


class RiverService(object):

    @staticmethod
    def create(schema):
        valid = RiverService.validate_schema(schema)
        if not valid:
            return None
        river = River()
        meta = schema['metadata']
        river.name = meta.get('name')
        river.description = meta.get('description')
        river.entry_point = meta.get('entry_point')
        river.raw_schema = json.dumps(schema)
        river.user = "ptbrodie"
        channel = Channel()
        channel.name = "%s/%s" % (river.user, river.name)
        river.ochannel = channel
        river.ichannels = []
        if schema['data']:
            for channel in RiverService.get_ichannels(schema):
                river.ichannels.append(channel)
        river.save()
        return river

    @staticmethod
    def validate_schema(schema):
        return True

    @staticmethod
    def get_ichannels(schema):
        # TODO: recursive case is to return all leaves
        channels = set()
        for k, v in schema['data'].items():
            if k == "_comment":
                continue
            channels.add(v.split('.')[0])
        res = []
        for channel in channels:
            res += Channel.get_by_name(channel)
        return res
