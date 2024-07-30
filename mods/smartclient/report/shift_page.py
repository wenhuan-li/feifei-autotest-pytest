from playwright.sync_api import Page, expect

from confs.smartclient_conf import SmartClientConf
from utils.assert_util import assert_dict, assert_none
from utils.playwright_util import set_checkbox
from utils.sql_server_util import SQLServerUtil

server: str = SmartClientConf().get(["database", "server"])
database: str = SmartClientConf().get(["database", "dbname"])
username: str = SmartClientConf().get(["database", "username"])
password: str = SmartClientConf().get(["database", "password"])
sql_util = SQLServerUtil(server, database, username, password)


class ShiftPage:

    def __init__(self, page: Page):
        self.page = page

    def open_page(self):
        """
        Function: \n
            打开班次设置页面
        """
        self.page.get_by_text("班次设置").click()
        expect(self.page.locator("h3")).to_have_text("班次设置")

    def add_shift(self, parameter):
        """
        Function: \n
            新增班次设置
        Parameter: \n
            alias(str):           班次别名
            begin_hh(str):        开始时间：小时
            begin_mm(str):        开始时间：分钟
            end_hh(str):          结束时间：小时
            end_mm(str):          结束时间：分钟
            is_over_day(bool):    是否跨天
        Example: \n
            {"alias":"测试班次","begin_hh":"18","begin_mm":"00","end_hh":"08","end_mm":"00","is_over_day":true}
        """
        self.page.get_by_text("添加").click()
        self.page.locator("//label[text()='班次名']/following-sibling::div//input").fill(parameter.get('alias'))
        self.page.locator("//label[text()='开始时间']/following-sibling::div//input[@placeholder='HH']").fill(
            parameter.get('begin_hh'))
        self.page.locator("//label[text()='开始时间']/following-sibling::div//input[@placeholder='MM']").fill(
            parameter.get('begin_mm'))
        self.page.locator("//label[text()='结束时间']/following-sibling::div//input[@placeholder='HH']").fill(
            parameter.get('end_hh'))
        self.page.locator("//label[text()='结束时间']/following-sibling::div//input[@placeholder='MM']").fill(
            parameter.get('end_mm'))
        set_checkbox(self.page, "//input[@ng-model='vm.current.scheduleSetting.isEndTimeNextDay']",
                     parameter.get('is_over_day'))
        self.page.locator("//button[text()='保存']").click()
        expect(self.page.locator("//div[text()='操作成功']")).to_be_visible()

    def set_shift(self, parameter):
        """
        Function: \n
            修改班次设置
        Parameter: \n
            alias(str):           班次别名
            alias_new(str):       修改后的班次别名
            begin_hh(str):        开始时间：小时
            begin_mm(str):        开始时间：分钟
            end_hh(str):          结束时间：小时
            end_mm(str):          结束时间：分钟
            is_over_day(bool):    是否跨天
        Example: \n
            {"alias":"测试班次","alias_new":"测试班次改","begin_hh":"18","begin_mm":"00","end_hh":"08","end_mm":"00","is_over_day":true}
        """
        self.page.locator(
            f"//td[contains(text(), '{parameter.get("alias")}')]/following-sibling::td//input[@value='编辑']").click()
        self.page.locator("//label[text()='班次名']/following-sibling::div//input").fill(parameter.get("alias_new"))
        self.page.locator("//label[text()='开始时间']/following-sibling::div//input[@placeholder='HH']").fill(
            parameter.get("begin_hh"))
        self.page.locator("//label[text()='开始时间']/following-sibling::div//input[@placeholder='MM']").fill(
            parameter.get("begin_mm"))
        self.page.locator("//label[text()='结束时间']/following-sibling::div//input[@placeholder='HH']").fill(
            parameter.get("end_hh"))
        self.page.locator("//label[text()='结束时间']/following-sibling::div//input[@placeholder='MM']").fill(
            parameter.get("end_mm"))
        set_checkbox(self.page, "//input[@ng-model='vm.current.scheduleSetting.isEndTimeNextDay']",
                     parameter.get("is_over_day"))
        self.page.locator("//button[text()='保存']").click()
        expect(self.page.locator("//div[text()='操作成功']")).to_be_visible()

    def del_shift(self, parameter):
        """
        Function: \n
            删除班次设置
        Parameter: \n
            alias(str):           班次别名
        Example: \n
            {"alias":"测试班次改"}
        """
        self.page.locator(
            f"//td[contains(text(), '{parameter.get("alias")}')]/following-sibling::td//input[@value='删除']").click()
        expect(self.page.get_by_text("删除确定框")).to_be_visible()
        self.page.locator("//button[text()='确定']").click()
        expect(self.page.locator(f"//td[contains(text(), '{parameter.get("alias")}')]")).not_to_be_visible()

    def assert_shift_exists(self, parameter):
        """
        Function: \n
            验证新增/修改的班次设置
        Parameter: \n
            alias(str):           班次别名
            begin_hh(str):        开始时间：小时
            begin_mm(str):        开始时间：分钟
            end_hh(str):          结束时间：小时
            end_mm(str):          结束时间：分钟
            is_over_day(bool):    是否跨天
        Example: \n
            {"alias":"测试班次","begin_hh":"18","begin_mm":"00","end_hh":"08","end_mm":"00","is_over_day":true}
        """
        expect(self.page.locator(f"//td[contains(text(), '{parameter.get("alias")}')]")).to_be_visible()
        expect(self.page.locator(
            f"//td[contains(text(), '{parameter.get("alias")}')]/following-sibling::td[contains(text(), '{parameter.get("begin_hh")}:{parameter.get("begin_mm")}')]")).to_be_visible()
        expect(self.page.locator(
            f"//td[contains(text(), '{parameter.get("alias")}')]/following-sibling::td[contains(text(), '{parameter.get("end_hh")}:{parameter.get("end_mm")}')]")).to_be_visible()
        actual_dict = {
            "ALIAS": parameter.get("alias"),
            "ISENDTIMENEXTDAY": str(int(parameter.get("is_over_day"))),
            "BEGINTIME": f"1970-01-01 {parameter.get("begin_hh")}:{parameter.get("begin_mm")}:00",
            "ENDTIME": f"1970-01-01 {parameter.get("end_hh")}:{parameter.get("end_mm")}:00",
        }
        stmt = f"SELECT * FROM tScheduleTimePeriod WHERE alias = '{parameter.get("alias")}'"
        expect_dict = sql_util.get_row_dict(stmt)
        assert_dict(actual_dict, expect_dict)

    def assert_shift_delete(self, parameter):
        """
        Function: \n
            验证删除班次后, 数据库数据被移除
        Parameter: \n
            alias(str):           班次别名
        Example: \n
            {"alias":"测试班次改"}
        """
        expect(self.page.locator(f"//td[contains(text(), '{parameter.get("alias")}')]")).not_to_be_visible()
        stmt = f"SELECT * FROM tScheduleTimePeriod WHERE alias = '{parameter.get("alias")}'"
        expect_dict = sql_util.get_row_dict(stmt)
        assert_none(expect_dict)
