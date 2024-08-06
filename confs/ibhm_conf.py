class IBHMConf:

    def __init__(self):
        self.conf_dict = {
            "frontend": {
                "host": "130.147.249.194",
                "port": 8091
            },
            "backend": {
                "host": "130.147.249.194",
                "port": 8084
            },
            "database": {
                "host": "130.147.249.194",
                "port": 5432,
                "dbname": "ehm",
                "username": "postgres",
                "password": "123"
            }
        }

    def get(self, keys):
        _dict = self.conf_dict
        for key in keys:
            if key not in _dict:
                return None
            _dict = _dict[key]
        return _dict