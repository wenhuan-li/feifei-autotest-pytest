import time

from pywinauto import Application


class LoginApp:

    def __init__(self, app):
        self.app = app

    def open_app(self, path=r"C:\GCRIS2Client\Kodak.GCRIS.exe"):
        self.app = Application().start(path)

    def close_app(self):
        time.sleep(5)
        self.app.kill()

    def login_app(self, parameter):
        self.app["KODAK GC RIS 3.0"]["Edit0"].type_keys(parameter.get("username"), with_spaces=True)
        self.app["KODAK GC RIS 3.0"]["Edit2"].type_keys(parameter.get("password"), with_spaces=True)
        self.app["KODAK GC RIS 3.0"]["Edit2"].type_keys("{ENTER}")
