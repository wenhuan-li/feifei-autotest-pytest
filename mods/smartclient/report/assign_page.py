from playwright.sync_api import Page, expect

from confs.smartclient_conf import SmartClientConf
from utils.assert_util import assert_dict
from utils.playwright_util import set_checkbox
from utils.sql_server_util import SQLServerUtil

server: str = SmartClientConf().get(["database", "server"])
database: str = SmartClientConf().get(["database", "dbname"])
username: str = SmartClientConf().get(["database", "username"])
password: str = SmartClientConf().get(["database", "password"])
sql_util = SQLServerUtil(server, database, username, password)

assign_mode_dict = {"周期分发": "1", "实时分发": "2"}
undone_policy_dict = {"无": "0", "分发给下一班次": "1", "分发给当前班次": "2", "回撤后不直接重发": "3", "不回撤只发提醒GW事件": "4"}


class AssignPage:

    def __init__(self, page: Page):
        self.page = page

    def open_page(self):
        """
        Function: \n
            打开组分发设置页面
        """
        self.page.get_by_text("分发设置").click()
        expect(self.page.locator("//label[@for='exampleInputEmail2']")).to_have_text("报告类型")

    def set_assign(self, parameter):
        """
        Function: \n
            修改组的分发设置
        Parameter: \n
            group_name(str):                组名
            max_percent(str):               组管理员
            max_hold_weight_today(str):     组内个人分发上限
            assign_mode(str):               分发模式: 周期分发, 实时分发
            success_send_gateway(bool):     正常分发时是否发gateway
            failure_send_gateway(bool):     分发失败时是否发gateway
            reassign_send_gateway(bool):    补发时是否发gateway
            withdraw_send_gateway(bool):    撤回时是否发gateway
            undone_policy(str):             未完成任务处理: 无, 分发给下一班次, 分发给当前班次, 回撤后不直接重发, 不回撤只发提醒GW事件
        Example: \n
            {"group_name":"测试写入组","max_percent":"90","max_hold_weight_today":"1","assign_mode":"周期分发","success_send_gateway":true,"failure_send_gateway":true,"reassign_send_gateway":true,"withdraw_send_gateway":true,"undone_policy":"分发给下一班次"}
        """
        self.page.locator(f"//td[@title='{parameter.get("group_name")}']/following-sibling::td//button[text()='编辑']").click()
        self.page.locator("//input[@ng-model='vm.current.groupSetting.maxPercentage']").fill(parameter.get("max_percent"))
        self.page.locator("//input[@ng-model='vm.current.groupSetting.maxHoldWeightToday']").fill(parameter.get("max_hold_weight_today"))
        self.page.select_option("select[ng-model='vm.current.groupSetting.assignMode']", label=parameter.get("assign_mode"))
        set_checkbox(self.page, "//input[@ng-model='vm.current.groupSetting.sendGatewayFirst']", parameter.get("success_send_gateway"))
        set_checkbox(self.page, "//input[@ng-model='vm.current.groupSetting.sendGatewaySecond']", parameter.get("failure_send_gateway"))
        set_checkbox(self.page, "//input[@ng-model='vm.current.groupSetting.sendGatewayThird']", parameter.get("reassign_send_gateway"))
        set_checkbox(self.page, "//input[@ng-model='vm.current.groupSetting.sendGatewayForWithdraw']",
                     parameter.get("withdraw_send_gateway"))
        self.page.select_option("select[ng-model='vm.current.groupSetting.processUndoneTaskPolicy']",
                                label=parameter.get("undone_policy"))
        self.page.locator("//button[text()='保存']").click()

    def assert_assign(self, parameter):
        """
        Function: \n
            验证修改组的分发设置
        Parameter: \n
            group_name(str):                组名
            max_percent(str):               组管理员
            max_hold_weight_today(str):     组内个人分发上限
            assign_mode(str):               分发模式: 周期分发, 实时分发
            success_send_gateway(bool):     正常分发时是否发gateway
            failure_send_gateway(bool):     分发失败时是否发gateway
            reassign_send_gateway(bool):    补发时是否发gateway
            withdraw_send_gateway(bool):    撤回时是否发gateway
            undone_policy(str):             未完成任务处理: 无, 分发给下一班次, 分发给当前班次, 回撤后不直接重发, 不回撤只发提醒GW事件
        Example: \n
            {"group_name":"测试写入组","max_percent":"90","max_hold_weight_today":"1","assign_mode":"周期分发","success_send_gateway":true,"failure_send_gateway":true,"reassign_send_gateway":true,"withdraw_send_gateway":true,"undone_policy":"分发给下一班次"}
        """
        expect(self.page.locator(f"//td[@title='{parameter.get("group_name")}']")).to_be_visible()
        stmt = f"SELECT GROUPGUID FROM tGroup WHERE GroupName = '{parameter.get('group_name')}'"
        guid = sql_util.get_row_dict(stmt)["GROUPGUID"]
        binary = f"{int(parameter.get('success_send_gateway'))}{int(parameter.get('failure_send_gateway'))}{int(parameter.get('reassign_send_gateway'))}{int(parameter.get('withdraw_send_gateway'))}"
        actual_dict = {
            "GROUPGUID": guid,
            "MAXPERCENTAGE": parameter.get("max_percent"),
            "MAXHOLDWEIGHTTODAY": parameter.get("max_hold_weight_today"),
            "ASSIGNMODE": assign_mode_dict[parameter.get("assign_mode")],
            "PROCESSUNDONETASKPOLICY": undone_policy_dict[parameter.get("undone_policy")],
            "SENDGATEWAY": str(int(binary, 2))
        }
        stmt = f"SELECT * FROM tGroupSetting WHERE GroupGuid = '{guid}'"
        expect_dict = sql_util.get_row_dict(stmt)
        assert_dict(actual_dict, expect_dict, message=f"{parameter.get('step_name')}")
