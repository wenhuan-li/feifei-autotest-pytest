from playwright.sync_api import expect, Page

from confs.smartclient_conf import SmartClientConf

host: str = SmartClientConf().get(["output", "host"])
port: int = SmartClientConf().get(["output", "port"])
base_url = f"http://{host}:{port}"


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

    def open_page(self, url=f"{base_url}/#/login"):
        """
        Function: \n
            打开报告分发系统
        """
        self.page.goto(url)

    def login(self, parameter):
        """
        Function: \n
            登录报告分发系统
        Parameter: \n
            username(str): 用户名
            password(str): 密码
        Example: \n
            {"username":"demo","password":"demo"}
        """
        self.page.get_by_placeholder("登录名").fill(parameter["username"])
        self.page.get_by_placeholder("密码").fill(parameter["password"])
        self.page.get_by_text("登录").click()

    def assert_login_ok(self):
        """
        Function: \n
            验证登录报告分发系统是否成功
        """
        expect(self.page.locator("h2")).to_have_text("报告分发 (按放射编号分发)")

    def login_ok(self, parameter):
        """
        Function: \n
            登录报告分发系统, 并附带验证
        Parameter: \n
            username(str): 用户名
            password(str): 密码
        Example: \n
            {"username":"demo","password":"demo"}
        """
        self.login(parameter)
        self.assert_login_ok()
