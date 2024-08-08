from confs.ibhm_conf import IBHMConf
from utils.assert_util import assert_dict, assert_list
from utils.http_util import HttpUtil
from utils.pg_server_util import PgServerUtil

host: str = IBHMConf().get(["backend", "host"])
port: int = IBHMConf().get(["backend", "port"])
db_host: str = IBHMConf().get(["database", "host"])
db_port: int = IBHMConf().get(["database", "port"])
database: str = IBHMConf().get(["database", "dbname"])
username: str = IBHMConf().get(["database", "username"])
password: str = IBHMConf().get(["database", "password"])
base_url = f"http://{host}:{port}/api/detail"
connector = PgServerUtil(db_host, db_port, database, username, password)


class DeviceDetail:

    def __init__(self):
        pass

    def assessment(self, parameter):
        url = f"{base_url}/assessment"
        params = {
            "modality": parameter.get("modality"),
            "serialNum": parameter.get("serialNum")
        }
        actual = HttpUtil().get(url, params=params).get("content")[0]
        expect = connector.connect().execute(parameter.get("query"))[0]
        assert_dict(actual, expect, description=parameter)
        return self

    def assessment_detail_fields(self, parameter):
        url = f"{base_url}/assessment"
        params = {
            "modality": parameter.get("modality"),
            "serialNum": parameter.get("serialNum")
        }
        actual = HttpUtil().get(url, params=params).get("content")[0].get("detailFields")
        record = connector.connect().execute(parameter.get("query"))[0]
        expect = []
        for key, values in record.items():
            question_key, title = key.split(";")
            value = "" if not values else values.split(";")
            if "" == values: value = [""]
            expect.append({
                "questionKey": question_key,
                "title": title,
                "value": value
            })
        assert_list(actual, expect, description=parameter)
        return self
