class SmartClientConf:

    def __init__(self):
        self.conf_dict = {
            "output": {
                "host": "130.147.249.216",
                "port": 27447
            },
            "database": {
                "server": "130.147.249.216",
                "dbname": "GCRIS2",
                "username": "sa",
                "password": "sa_2007"
            }
        }

    def get(self, keys):
        _dict = self.conf_dict
        for key in keys:
            if key not in _dict:
                return None
            _dict = _dict[key]
        return _dict
