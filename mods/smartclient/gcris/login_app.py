from pywinauto import Application


class LoginAPP:

    def __init__(self, app):
        self.app = app

    def open_app(self, path=r"C:\GCRIS2Client\Kodak.GCRIS.exe"):
        self.app = Application().start(path)