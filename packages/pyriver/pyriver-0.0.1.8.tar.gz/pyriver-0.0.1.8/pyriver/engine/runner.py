class RiverRunner(object):

    def __init__(self, schema):
        pass

    @staticmethod
    def get_ichannels(schema):
        # TODO: recursive case is to return all leaves
        channels = set()
        for k, v in schema['data'].iteritems():
            if k == "_comment":
                continue
            channels.add(v.split('.')[0])
        return channels

    @staticmethod
    def get_ochannel(schema):
        # TODO: should this be the repo, package name, or unique channel name?
        user = schema['metadata']['user']
        name = schema['metadata']['name']
        return "%s/%s" % (user, name)

    @staticmethod
    def get_interval(schema):
        return schema['metadata']['interval']

    def process(self, event):
        res = {}
        res['rainfall'] = event['data']['rainfall']
        res['temp_range'] = round(event['data']['high_temp'] - event['data']['low_temp'], 2)
        res['revenue_per_acre'] = round(event['data']['cost_per_pound'] * event['data']['pounds_per_acre'], 2)
        return res

    def run(self):
        manager = RiverManager(self)
        manager.run()
