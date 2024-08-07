from datetime import datetime

from confs.ibhm_conf import IBHMConf
from utils.assert_util import assert_string, assert_dict, assert_list
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


def conv_area_cn_en(area):
    areas = {"EAST_DISTRICT": "东区", "WEST_DISTRICT": "西区", "SOUTH_DISTRICT": "南区", "NORTH_DISTRICT": "北区",
             "ALL": "全国"}
    for key, value in areas.items():
        if value == area:
            return key
    return None


def conv_time_en_int(time_condition):
    times = {"month": 30, "three_month": 90, "six_month": 180, "year": 365, "all": 9999}
    for key, value in times.items():
        if key == time_condition:
            return value
    return None


class Dashboard:

    def __init__(self):
        pass

    def get_latest_data_update_time(self, parameter):
        url = f"{base_url}/getLatestDataUpdateTime"
        actual = HttpUtil().get(url)
        actual = actual.get("content").get("latestDataUpdateTime").replace("T", " ")
        expect = connector.connect().execute(parameter.get("query"))
        expect = datetime.strftime(expect[0]["max_create_at"], "%Y-%m-%d %H:%M:%S")
        assert_string(actual, expect, description=parameter)
        return self

    def dashboard_ib(self, parameter):
        url = f"{base_url}/ib"
        actual = HttpUtil().get(url, params={"area": parameter.get("area")}).get("content")
        record = connector.connect().execute(parameter.get("query"))
        expect = {}
        total = 0
        for item in record:
            modality = item["modality"].lower()
            key = f"ib{modality.capitalize()}Num"
            expect[key] = item["count"]
            total += item["count"]
        expect["ibTotal"] = total
        assert_dict(actual, expect, description=parameter)
        return self

    def modality_health_status(self, parameter):
        url = f"{base_url}/modality/health_status"
        area = parameter.get("area", None)
        modality = parameter.get("modality", None)
        time_condition = parameter.get("time_condition", "month")
        params = {
            "area": area,
            "modality": modality,
            "time_condition": time_condition
        }
        actual = HttpUtil().get(url, params=params).get("content")
        expect = connector.connect().execute(parameter.get("query"))
        expect = [{"deviceNum": item["count"], "healthStatus": item["health_status"]} for item in expect]
        assert_list(actual, expect, description=parameter)
        return self
