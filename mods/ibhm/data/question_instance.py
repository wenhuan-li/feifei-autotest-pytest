from datetime import datetime

import pytest

from confs.ibhm_conf import IBHMConf
from utils.assert_util import assert_dict
from utils.file_util import pd_read_datas
from utils.pg_server_util import PgServerUtil

db_host: str = IBHMConf().get(["database", "host"])
db_port: int = IBHMConf().get(["database", "port"])
database: str = IBHMConf().get(["database", "dbname"])
username: str = IBHMConf().get(["database", "username"])
password: str = IBHMConf().get(["database", "password"])
connector = PgServerUtil(db_host, db_port, database, username, password)
ct_rename_columns = {
    '开始时间': 'start_time',
    'Start time': 'start_time',
    '完成时间': 'completion_time',
    'Completion time': 'completion_time',
    '电子邮件': 'email',
    'Email': 'email',
    '名称': 'name',
    'Name': 'name',
    '区域': 'area',
    'Modality': 'modality',
    '设备号': 'serial_num',
    'SDL': 'sdl',
    '设备型号': 'device_version',
    '医院名称': 'hospital',
    '综合评分': 'score',
    '健康状态': 'health_status',
    '关注度': 'attention',
    '跟踪更新': 'track_desc',
    '核心硬件/软件隐患': 'ct_00002',
    '“核心硬件/软件隐患"的细节描述': 'ct_00003',
    '当前球管安装时间': 'ct_00004',
    '当前球管曝光秒': 'ct_00005',
    '球管类型': 'ct_00006',
    '是否已上传TubeHistory文件': 'ct_00007',
    '设备故障次数': 'ct_00008',
    '附件与其他零部件': 'ct_00009',
    '"附件与其他零部件"的细节描述': 'ct_00010',
    '设备运行负荷': 'ct_00011',
    '设备使用年限': 'ct_00012',
    '设备操作应用': 'ct_00013',
    '"设备操作应用"的细节描述': 'ct_00014',
    '场地与使用环境': 'ct_00015',
    '设备日常保养情况': 'ct_00016',
    '"设备日常情况"的细节描述': 'ct_00017',
    '外设与第三方设备': 'ct_00018',
    '"外设与第三方设备"的细节描述': 'ct_00019',
    '网络连接情况': 'ct_00020',
    '其他': 'ct_00021',
    '核心打分': 'ct_00022',
    '故障次数打分': 'ct_00023',
    '附件打分': 'ct_00024',
    '负荷打分': 'ct_00025',
    '年限打分': 'ct_00026',
    '操作打分': 'ct_00027',
    '环境打分': 'ct_00028',
    '保养情况打分': 'ct_00029',
    '外设打分': 'ct_00030',
    '网络打分': 'ct_00031'
}


class QuestionInstance:

    def __init__(self):
        pass

    def ct_question_instance(self, parameter):
        ct_question_datas = pd_read_datas(parameter.get("file"), parameter.get("sheet"), columns=ct_rename_columns)
        for actual in ct_question_datas:
            serial_num = actual.get("serial_num")
            completion_time = actual.get("completion_time")
            if all(not actual.get(key) for key in ["sdl", "hospital", "device_version"]):
                query = f"SELECT sdl, hospital, device_version FROM t_ib_information WHERE serial_number = '{serial_num}'"
                extra = connector.connect().execute(query)[0]
                if extra:
                    actual["sdl"] = extra.get("sdl")
                    actual["hospital"] = extra.get("hospital")
                    actual["device_version"] = extra.get("device_version")
            actual = {key: str(value) if isinstance(value, int) else value for key, value in actual.items()}
            actual = {key: value.strip() if isinstance(value, str) else value for key, value in actual.items()}
            actual = {key: f"{value:.2f}".rstrip("0").rstrip(".") if isinstance(value, float) else value for key, value in actual.items()}
            actual = {key: (None if value in ["nan"] else value) for key, value in actual.items()}
            actual = {
                key: datetime.strptime(value, "%m/%d/%y %H:%M:%S")
                if key in ["start_time", "completion_time"] and isinstance(value, str) else value
                for key, value in actual.items()
            }
            query = f"SELECT * FROM t_questionnaire_instance WHERE serial_num = '{serial_num}' AND completion_time = '{completion_time}'"
            record = connector.connect().execute(query)
            pytest.assume(record, f"Data not found ==> {query}")
            expect = record[0]
            expect = {key: value.rstrip("0").rstrip(".") if value in ["0.0", "1.0"] else value for key, value in expect.items()}
            assert_dict(actual, expect, message=f"{serial_num}, {completion_time}")
        return self
