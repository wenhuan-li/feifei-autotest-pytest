from playwright.sync_api import Page, expect

from confs.smartclient_conf import SmartClientConf
from utils.assert_util import assert_dict, assert_list
from utils.playwright_util import set_multi_select
from utils.sql_server_util import SQLServerUtil

server: str = SmartClientConf().get(["database", "server"])
database: str = SmartClientConf().get(["database", "dbname"])
username: str = SmartClientConf().get(["database", "username"])
password: str = SmartClientConf().get(["database", "password"])
sql_util = SQLServerUtil(server, database, username, password)


class GroupPage:

    def __init__(self, page: Page):
        self.page = page

    def open_page(self):
        """
        Function: \n
            打开组管理设置页面
        """
        self.page.get_by_text("组管理").first.click()
        expect(self.page.locator("//div/h1[text()='组管理']")).to_be_visible()

    def add_write_group(self, parameter):
        """
        Function: \n
            新增写入组设置
        Parameter: \n
            group_name(str):    组名
            admins(list):       组管理员
            modalities(list):   组偏好设置/偏好的设备类型
            attribute(str):     组偏好设置/偏好的设备属性
            devices(list):      组偏好设置/偏好的设备
            physios(list):      组偏好设置/偏好的生理系统
            bodyparts(list):    组偏好设置/偏好的部位分类
            patients(list):     组偏好设置/偏好的病人类型
            billdepts(list):    组偏好设置/偏好的开单科室
            referral(str):      组偏好设置/偏好的转诊类型: 非转诊, 转诊出去, 转诊进来
            sources(list):      组偏好设置/任务来源站点
            depts(list):        组成员/选范围
            crews(list):        组成员/选组员
        Example: \n
            {"group_name":"测试写入组","admins":["刘思思(LSS)"],"modalities":["CR","CT"],"attribute":"平扫","devices":["CR3"],"physios":["头颈部"],"bodyparts":["30上肢"],"patients":["急诊病人"],"billdepts":["体检中心"],"referral":"非转诊","sources":["site1"],"depts":["aDep1"],"crews":["aHL1(aHL1)","aHL2(aHL2)","aHL3(aHL3)"]}
        """
        self.page.locator("//h1[text()='写']").click()
        self.page.locator("//button[text()='添加']").click()
        self.page.locator("//label[text()='*组名:']/following-sibling::div//input").fill(parameter.get("group_name"))
        set_multi_select(self.page, "//label[text()='组管理员']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("admins"))

        # 设置组偏好
        self.page.locator("//button[text()='组偏好...']").click()
        set_multi_select(self.page, "//label[text()='偏好的设备类型:']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("modalities"))
        self.page.locator("//label[text()='偏好的设备属性:']/following-sibling::div//select").click()
        self.page.select_option("select[ng-model='vm.current.modalityProperty']", label=parameter.get("attribute"))
        set_multi_select(self.page, "//label[text()='偏好的设备:']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("devices"))
        set_multi_select(self.page, "//label[text()='偏好的生理系统:']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("physios"))
        set_multi_select(self.page, "//label[text()='偏好的部位分类:']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("bodyparts"))

        """
        以下两步无法保存, 暂存
        self.page.locator("//label[text()='偏好的检查标签1:']/following-sibling::div//input").fill(tag1)
        self.page.locator("//label[text()='偏好的检查标签2:']/following-sibling::div//input").fill(tag2)
        """

        set_multi_select(self.page, "//label[text()='偏好的病人类型:']/following-sibling::div//input",
                         "//ul/li/div/a/span[contains(text(), '#child')]", parameter.get("patients"))
        set_multi_select(self.page, "//label[text()='偏好的开单科室:']/following-sibling::div//input",
                         "//ul/li/div/a/span[contains(text(), '#child')]", parameter.get("billdepts"))
        self.page.locator("//label[text()='偏好的转诊类型:']/following-sibling::div//select").click()
        self.page.select_option("select[ng-model='vm.current.referralType']", label=parameter.get("referral"))
        set_multi_select(self.page, "//label[text()='任务来源站点:']/following-sibling::div//input",
                         "//ul/li/div/a/span[contains(text(), '#child')]", parameter.get("sources"))
        self.page.locator("//button[text()='确认']").click()

        # 设置组成员
        self.page.locator("//button[text()='组成员']").click()
        for dept in parameter.get("depts"):
            self.page.locator(f"//ul/li/a/span[text()='{dept}']").first.click()
        for crew in parameter.get("crews"):
            self.page.locator(f"//ul/li/a/span[text()='{crew}']").first.click()
        self.page.locator("//button[text()='>>']").click()
        self.page.locator("//button[text()='确认']").click()
        self.page.locator("//button[text()='保存']").click()

    def add_audit_group(self, parameter):
        """
        Function: \n
            新增写入组设置
        Parameter: \n
            group_name(str):    组名
            admins(list):       组管理员
            modalities(list):   组偏好设置/偏好的设备类型
            attribute(str):     组偏好设置/偏好的设备属性
            devices(list):      组偏好设置/偏好的设备
            physios(list):      组偏好设置/偏好的生理系统
            bodyparts(list):    组偏好设置/偏好的部位分类
            patients(list):     组偏好设置/偏好的病人类型
            billdepts(list):    组偏好设置/偏好的开单科室
            referral(str):      组偏好设置/偏好的转诊类型: 非转诊, 转诊出去, 转诊进来
            sources(list):      组偏好设置/任务来源站点
            depts(list):        组成员/选范围
            crews(list):        组成员/选组员
        Example: \n
            {"group_name":"测试审核组","admins":["刘思思(LSS)"],"modalities":["CR","CT"],"attribute":"平扫","devices":["CR3"],"physios":["头颈部"],"bodyparts":["30上肢"],"patients":["急诊病人"],"billdepts":["体检中心"],"referral":"非转诊","sources":["site1"],"depts":["aDep1"],"crews":["aHL1(aHL1)","aHL2(aHL2)","aHL3(aHL3)"]}
        """
        self.page.locator("//h1[text()='审']").click()
        self.page.locator("//button[text()='添加']").click()
        self.page.locator("//label[text()='*组名:']/following-sibling::div//input").fill(parameter.get("group_name"))
        set_multi_select(self.page, "//label[text()='组管理员']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("admins"))

        # 设置组偏好
        self.page.locator("//button[text()='组偏好...']").click()
        set_multi_select(self.page, "//label[text()='偏好的设备类型:']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("modalities"))
        self.page.locator("//label[text()='偏好的设备属性:']/following-sibling::div//select").click()
        self.page.select_option("select[ng-model='vm.current.modalityProperty']", label=parameter.get("attribute"))
        set_multi_select(self.page, "//label[text()='偏好的设备:']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("devices"))
        set_multi_select(self.page, "//label[text()='偏好的生理系统:']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("physios"))
        set_multi_select(self.page, "//label[text()='偏好的部位分类:']/following-sibling::div//input",
                         "//ul/li/div/a/span[text()='#child']", parameter.get("bodyparts"))

        """
        以下两步无法保存, 暂存
        self.page.locator("//label[text()='偏好的检查标签1:']/following-sibling::div//input").fill(tag1)
        self.page.locator("//label[text()='偏好的检查标签2:']/following-sibling::div//input").fill(tag2)
        """

        set_multi_select(self.page, "//label[text()='偏好的病人类型:']/following-sibling::div//input",
                         "//ul/li/div/a/span[contains(text(), '#child')]", parameter.get("patients"))
        set_multi_select(self.page, "//label[text()='偏好的开单科室:']/following-sibling::div//input",
                         "//ul/li/div/a/span[contains(text(), '#child')]", parameter.get("billdepts"))
        self.page.locator("//label[text()='偏好的转诊类型:']/following-sibling::div//select").click()
        self.page.select_option("select[ng-model='vm.current.referralType']", label=parameter.get("referral"))
        set_multi_select(self.page, "//label[text()='任务来源站点:']/following-sibling::div//input",
                         "//ul/li/div/a/span[contains(text(), '#child')]", parameter.get("sources"))
        self.page.locator("//button[text()='确认']").click()

        # 设置组成员
        self.page.locator("//button[text()='组成员']").click()
        for dept in parameter.get("depts"):
            self.page.locator(f"//ul/li/a/span[text()='{dept}']").first.click()
        for crew in parameter.get("crews"):
            self.page.locator(f"//ul/li/a/span[text()='{crew}']").first.click()
        self.page.locator("//button[text()='>>']").click()
        self.page.locator("//button[text()='确认']").click()
        self.page.locator("//button[text()='保存']").click()

    def delete_group(self, parameter):
        """
        Function: \n
            删除存在的组设置
        Parameter: \n
            group_name(str):    组名
        Example: \n
            {"group_name":"测试写入组"}
        """
        self.page.locator(f"//table/tbody/tr/td[text()='{parameter.get("group_name")} ']").click()
        self.page.locator("//button[text()='删除']").click()
        self.page.locator("//button[text()='确定']").click()
        self.page.reload()

    def assert_write_group(self, parameter):
        """
        Function: \n
            验证新增/修改的写入组的设置
        Parameter: \n
            group_name(str):    组名
            admins(list):       组管理员
            modalities(list):   组偏好设置/偏好的设备类型
            attribute(str):     组偏好设置/偏好的设备属性
            devices(list):      组偏好设置/偏好的设备
            physios(list):      组偏好设置/偏好的生理系统
            bodyparts(list):    组偏好设置/偏好的部位分类
            patients(list):     组偏好设置/偏好的病人类型
            billdepts(list):    组偏好设置/偏好的开单科室
            referral(str):      组偏好设置/偏好的转诊类型: 非转诊, 转诊出去, 转诊进来
            sources(list):      组偏好设置/任务来源站点
            depts(list):        组成员/选范围
            crews(list):        组成员/选组员
        Example: \n
            {"group_name":"测试写入组","admins":["刘思思(LSS)"],"modalities":["CR"],"attribute":"平扫","devices":["CR3"],"physios":["头颈部"],"bodyparts":["30上肢"],"patients":["急诊病人"],"billdepts":["体检中心"],"referral":"非转诊","sources":["site1"],"depts":["aDep1"],"crews":["aHL1(aHL1)","aHL2(aHL2)","aHL3(aHL3)"]}
        """
        expect(self.page.locator(f"//td[contains(text(), '{parameter.get("group_name")} ')]")).to_be_visible()
        # tGroup表验证
        actual_group = {
            "GROUPNAME": parameter.get("group_name"),
            "TYPE": "UnwrittenReport",
            "DEPT": ",".join(parameter.get("depts")[::-1]),
            "TIMEPERIODGROUPNAME": "默认班次组",
            "GROUPMANAGERGUID": ",".join(
                item.replace(item[item.find('('):item.find(')') + 1], '') for item in parameter.get("admins")),
            "GROUPMANAGERNAME": ",".join(
                item.replace(item[item.find('('):item.find(')') + 1], '') for item in parameter.get("admins")),
        }
        stmt = f"SELECT * FROM tGroup WHERE GroupName = '{parameter.get("group_name")}'"
        expect_group = sql_util.get_row_dict(stmt)
        assert_dict(actual_group, expect_group)

        # tGroupSetting表验证
        sites = []
        for source in parameter.get("sources"):
            stmt = f"SELECT site FROM tSiteList WHERE alias = '{source}'"
            site = sql_util.get_row_dict(stmt)["SITE"]
            sites.append(site)
        actual_setting = {
            "PREFERRED_MODALITY_TYPE": ",".join(parameter.get("modalities")),
            "PREFERRED_MODALITY": ",".join(parameter.get("devices")),
            "PREFERRED_PHYSIOLOGICAL_SYSTEM": ",".join(parameter.get("physios")),
            "PREFERRED_PATIENT_TYPE": ",".join(parameter.get("patients")),
            "PREFERRED_SITE": ",".join(sites),
            "PREFERRED_BODAYPART_CATEGORY": ",".join(parameter.get("bodyparts")),
            "PREFERRED_APPLY_DEPT": ",".join(parameter.get("billdepts"))
        }
        group_guid = expect_group["GROUPGUID "]
        stmt = f"SELECT * FROM tGroupSetting WHERE GroupGuid = '{group_guid}'"
        expect_setting = sql_util.get_row_dict(stmt)
        assert_dict(actual_setting, expect_setting)

        # tGroupPeople表验证
        actual_people = [{"DOCTOR_NAME": crew, "GROUPNAME": parameter.get("group_name")} for crew in
                         parameter.get("crews")]
        stmt = f"SELECT * FROM tGroupPeople WHERE GroupGuid = '{group_guid}' ORDER BY DOCTOR_NAME"
        expect_people = sql_util.get_rows_dict(stmt)
        assert_list(actual_people, expect_people)

    def assert_audit_group(self, parameter):
        """
        Function: \n
            验证新增/修改的审核组的设置
        Parameter: \n
            group_name(str):    组名
            admins(list):       组管理员
            modalities(list):   组偏好设置/偏好的设备类型
            attribute(str):     组偏好设置/偏好的设备属性
            devices(list):      组偏好设置/偏好的设备
            physios(list):      组偏好设置/偏好的生理系统
            bodyparts(list):    组偏好设置/偏好的部位分类
            patients(list):     组偏好设置/偏好的病人类型
            billdepts(list):    组偏好设置/偏好的开单科室
            referral(str):      组偏好设置/偏好的转诊类型: 非转诊, 转诊出去, 转诊进来
            sources(list):      组偏好设置/任务来源站点
            depts(list):        组成员/选范围
            crews(list):        组成员/选组员
        Example: \n
            {"group_name":"测试审核组","admins":["刘思思(LSS)"],"modalities":["CR"],"attribute":"平扫","devices":["CR3"],"physios":["头颈部"],"bodyparts":["30上肢"],"patients":["急诊病人"],"billdepts":["体检中心"],"referral":"非转诊","sources":["site1"],"depts":["aDep1"],"crews":["aHL1(aHL1)","aHL2(aHL2)","aHL3(aHL3)"]}
        """
        expect(self.page.locator(f"//td[contains(text(), '{parameter.get("group_name")} ')]")).to_be_visible()
        # tGroup表验证
        actual_group = {
            "GROUPNAME": parameter.get("group_name"),
            "TYPE": "UnapprovedReport",
            "DEPT": ",".join(parameter.get("depts")[::-1]),
            "TIMEPERIODGROUPNAME": "默认班次组",
            "GROUPMANAGERGUID": ",".join(
                item.replace(item[item.find('('):item.find(')') + 1], '') for item in parameter.get("admins")),
            "GROUPMANAGERNAME": ",".join(
                item.replace(item[item.find('('):item.find(')') + 1], '') for item in parameter.get("admins")),
        }
        stmt = f"SELECT * FROM tGroup WHERE GroupName = '{parameter.get("group_name")}'"
        expect_group = sql_util.get_row_dict(stmt)
        assert_dict(actual_group, expect_group)

        # tGroupSetting表验证
        sites = []
        for source in parameter.get("sources"):
            stmt = f"SELECT site FROM tSiteList WHERE alias = '{source}'"
            site = sql_util.get_row_dict(stmt)["SITE"]
            sites.append(site)
        actual_setting = {
            "PREFERRED_MODALITY_TYPE": ",".join(parameter.get("modalities")),
            "PREFERRED_MODALITY": ",".join(parameter.get("devices")),
            "PREFERRED_PHYSIOLOGICAL_SYSTEM": ",".join(parameter.get("physios")),
            "PREFERRED_PATIENT_TYPE": ",".join(parameter.get("patients")),
            "PREFERRED_SITE": ",".join(sites),
            "PREFERRED_BODAYPART_CATEGORY": ",".join(parameter.get("bodyparts")),
            "PREFERRED_APPLY_DEPT": ",".join(parameter.get("billdepts"))
        }
        group_guid = expect_group["GROUPGUID "]
        stmt = f"SELECT * FROM tGroupSetting WHERE GroupGuid = '{group_guid}'"
        expect_setting = sql_util.get_row_dict(stmt)
        assert_dict(actual_setting, expect_setting)

        # tGroupPeople表验证
        actual_people = [{"DOCTOR_NAME": crew, "GROUPNAME": parameter.get("group_name")} for crew in
                         parameter.get("crews")]
        stmt = f"SELECT * FROM tGroupPeople WHERE GroupGuid = '{group_guid}' ORDER BY DOCTOR_NAME"
        expect_people = sql_util.get_rows_dict(stmt)
        assert_list(actual_people, expect_people)
