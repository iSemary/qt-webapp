import sys, os
# Importing PyQt5 Libs
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore, QtWidgets, QtWebEngineWidgets, QtPrintSupport
from PyQt5.QtGui import QMovie, QKeySequence
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
# For Making Task bar (icon and name displayed)
import ctypes
import datetime

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class LoadingScreen(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 315)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.label_animation = QLabel(self)
        # Splash image
        self.movie = QMovie('assets/SplashScreen.png')
        self.label_animation.setMovie(self.movie)
        timer = QTimer(self)
        self.movie.start()
        timer.singleShot(3000, self.stopAnimation)
        self.show()

    def stopAnimation(self):
        self.movie.stop()
        self.close()


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.loading_screen = LoadingScreen()

        layout = QtWidgets.QHBoxLayout(self)
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setContextMenuPolicy(Qt.NoContextMenu)

        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)
        self.page = QtWebEngineWidgets.QWebEnginePage(self)
        self.view.setPage(self.page)
        # Your Web App URL
        self.view.load(QtCore.QUrl("https://www.google.com/")) 
        self.page.printRequested.connect(self.printRequested)
        self.view.page().profile().downloadRequested.connect(self.on_downloadRequested)
        self.shortcut = QShortcut(QKeySequence("F11"), self)
        self.shortcut.activated.connect(self.toggleFullScreen)
        self.showMaximized()

    # _blank Request

    # Download .xlsx / CSV / PDF
    def on_downloadRequested(self, download):
        old_path = download.url().path()  # download.path()
        old_path_string = old_path.split("/")

        if old_path_string[-1] == 'excel':
            file_type = 'xlsx'
        elif old_path_string[-1] == 'csv':
            file_type = 'csv'
        elif old_path_string[-1] == 'pdf':
            file_type = 'pdf'
        else:
            file_type = 'xlsx'

        date_now = datetime.datetime.now()
        file_name = old_path_string[-2].capitalize() + '-' + date_now.strftime("%Y") + '-' + date_now.strftime(
            "%m") + '-' + date_now.strftime("%d") + ' _' + date_now.strftime("%I") + '_' + date_now.strftime(
            "%M") + '_' + date_now.strftime("%S")

        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", file_name + "." + file_type, "." + file_type + suffix
        )
        if path:
            download.setPath(path)
            download.accept()

    # Get Print Request from JavaScript
    def printRequested(self):

        defaultPrinter = QtPrintSupport.QPrinter(QtPrintSupport.QPrinterInfo.defaultPrinter())
        dialog = QtPrintSupport.QPrintDialog(defaultPrinter, self)

        # dialog.exec()
        self._printer = dialog.printer()
        # High Resolution
        self._printer = QPrinter(QPrinter.HighResolution)
        # To Print PDF
        # self._printer.setOutputFileName("new.pdf")
        self.page.print(self._printer, self.printResult)
        return True

    # Get Print Request from JavaScript
    def printResult(self, success):
        del self._printer

    # Close Event Show Alert
    def closeEvent(self, event):
        exit_message = 'Are you sure you want to exit ?'
        resp = QMessageBox.question(
            self,
            'Save Changes',
            exit_message,
            QMessageBox.Yes,
            QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # Toggling Full Screen Mode
    def toggleFullScreen(self):
        # 0 -> normal / 2-> maximized / 4-> full-screen
        state = int(self.windowState())
        print(state)
        if state == 2:
            self.showFullScreen()
        else:
            self.showMaximized()


def main():
    BrandName = 'Qt Webapp'
    app = QApplication(sys.argv)
    QApplication.setApplicationName(BrandName)
    QApplication.setApplicationDisplayName(BrandName)
    QApplication.setApplicationVersion('3.0.1')
    app_window = MainWindow()
    app.setWindowIcon(QtGui.QIcon('assets/favicon.ico'))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
