import json
from datetime import datetime

from confs.ibhm_conf import IBHMConf
from utils.assert_util import assert_string
from utils.http_util import HttpUtil
from utils.pg_server_util import PgServerUtil

host: str = IBHMConf().get(["backend", "host"])
port: int = IBHMConf().get(["backend", "port"])
base_url = f"http://{host}:{port}/api/dashboard"
db_host: str = IBHMConf().get(["database", "host"])
db_port: int = IBHMConf().get(["database", "port"])
database: str = IBHMConf().get(["database", "dbname"])
username: str = IBHMConf().get(["database", "username"])
password: str = IBHMConf().get(["database", "password"])
connector = PgServerUtil(db_host, db_port, database, username, password)


class Dashboard:

    def __init__(self):
        pass

    def get_latest_data_update_time(self, parameter):
        url = f"{base_url}/getLatestDataUpdateTime"
        actual = HttpUtil().get(url)
        actual = actual.get("content").get("latestDataUpdateTime").replace("T", " ")
        expect = connector.connect().execute(parameter.get("expect"))
        expect = datetime.strftime(expect[0]["max_create_at"], "%Y-%m-%d %H:%M:%S")
        assert_string(actual, expect, "数据更新时间")
        return self
