from datetime import datetime

from confs.ibhm_conf import IBHMConf
from utils.assert_util import assert_string, assert_dict
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


def conv_area_cn_en(cn):
    area_dict = {"EAST_DISTRICT": "东区", "WEST_DISTRICT": "西区", "SOUTH_DISTRICT": "南区", "NORTH_DISTRICT": "北区",
                 "ALL": "全国"}
    for key, value in area_dict.items():
        if value == cn:
            return key
    return None


class Dashboard:

    def __init__(self):
        pass

    def get_latest_data_update_time(self):
        url = f"{base_url}/getLatestDataUpdateTime"
        actual = HttpUtil().get(url)
        actual = actual.get("content").get("latestDataUpdateTime").replace("T", " ")
        select = "SELECT MAX(completion_time) AS max_create_at FROM t_questionnaire_instance"
        expect = connector.connect().execute(select)
        expect = datetime.strftime(expect[0]["max_create_at"], "%Y-%m-%d %H:%M:%S")
        assert_string(actual, expect, description=select)
        return self

    def dashboard_ib(self, parameter):
        url = f"{base_url}/ib"
        area = parameter.get("area")
        actual = HttpUtil().get(url, params={"area": conv_area_cn_en(area)}).get("content")
        area = f"'东区','西区','南区','北区'" if area == "全国" else f"'{area}'"
        select = f"SELECT d.modality, count(*) FROM device_view d INNER JOIN ib_platinum_list_view ib ON d.serial_num = ib.equipment AND d.modality = ib.modality WHERE ib.platinum = true AND area IN ({area}) GROUP BY d.modality"
        result = connector.connect().execute(select)
        expect = {}
        total = 0
        for item in result:
            modality = item["modality"].lower()
            key = f"ib{modality.capitalize()}Num"
            expect[key] = item["count"]
            total += item["count"]
        expect["ibTotal"] = total
        assert_dict(actual, expect, description=select, message=f"白金保IB数据_{area}")
        return self
