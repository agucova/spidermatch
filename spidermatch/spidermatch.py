import sys, re
from PyQt6 import QtWidgets
from PyQt6 import uic
from qt_material import apply_stylesheet

class WelcomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        uic.loadUi('windows/welcome.ui', self)
        # Connect the save button to the save_token method
        self.api_save_button.clicked.connect(self.save_token)
        # Set input enter to submit button
        self.api_token_input.returnPressed.connect(self.save_token)
        self.show()

    def save_token(self):
        token_matcher = r"[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
        self.api_token: str = self.api_token_input.text()
        if self.api_token and re.match(token_matcher, self.api_token):
            self.close()
        else:
            self.api_token_input.setText("")
            self.api_token_input.setPlaceholderText("Token inválido")
            QtWidgets.QMessageBox.warning(self, "Error", "Token inválido")


if __name__ == "__main__":
    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = WelcomeWindow()

    # setup stylesheet
    apply_stylesheet(app, theme='dark_teal.xml')

    # run
    window.show()
    app.exec()
