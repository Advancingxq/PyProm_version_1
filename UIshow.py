import sys

from PyQt5.QtCore import pyqtSignal, QFile, QIODevice, QTextStream, QFileInfo
import os
import numpy as np

import model
import pnml_generate
import pnml_read
import pnml_show
import Log
import textedit

from PyQt5.QtGui import QImage, QPixmap

from UItest import *

from PyQt5.QtWidgets import *
from PyQt5 import Qt, QtGui
import cv2

class MyWindow(QMainWindow, Ui_MainWindow):
    signal_dirpath = pyqtSignal(str)  # 定义一个带参数的信号
    tab_num = 0
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):

        self.setWindowTitle("PyProm")

        self.action.triggered.connect(self.openFolder)  # 将按键与槽连接
        self.signal_dirpath.connect(self.showFolder)  # 将信号与槽连接

        self.treeWidget.itemDoubleClicked['QTreeWidgetItem*', 'int'].connect(self.function)

        self.actionVersion.triggered.connect(self.showVersion)

        self.actionNew_Ctrl_N.triggered.connect(self.newFile)

        self.action_3.triggered.connect(self.saveFile)

        self.actionsave_as.triggered.connect(self.saveasFile)

        self.actionClose_Tab.triggered.connect(self.closeTab)

        self.actionExit.triggered.connect(self.close)

        self.actioncopy.triggered.connect(self.copyFile)

        self.actionPaste.triggered.connect(self.pasteFile)

        self.actionCut.triggered.connect(self.cutContents)

        self.actionFind.triggered.connect(self.findContents)

        self.actionReplace.triggered.connect(self.replaceContents)

        self.actionRun.triggered.connect(self.runLog)

        self.actionLog_Generator.triggered.connect(self.generateLog)

        self.actionModel_Compare.triggered.connect(self.compareModel)

        self.action_2.triggered.connect(self.analyseIncidenceMatrix)

    def analyseIncidenceMatrix(self):
        value, ok = QInputDialog.getText(self, "Analyse Model Incidence Matrix", "Input Model:",
                                         QLineEdit.Normal,"PLEASE INPUT CONTENTS")

        place, transition, incidenceMatrix = pnml_read.read(value)

        output_str = ""
        output_str += 'place:\n'
        output_str += ' '.join(place)
        output_str += '\n'
        output_str += 'transition:\n'
        output_str += ' '.join(transition)
        output_str += '\n'
        output_str += 'incidenceMatrix:\n'
        for item in incidenceMatrix:
            output_str += str(item)
            output_str += '\n'

        self.echo(output_str)

    def compareModel(self):
        value1, ok = QInputDialog.getText(self, "Compare Model", "Model one:", QLineEdit.Normal,"PLEASE INPUT CONTENTS")
        value2, ok = QInputDialog.getText(self, "Compare Model", "Model two:", QLineEdit.Normal,"PLEASE INPUT CONTENTS")
        place1, transition1, incidenceMatrix1 = pnml_read.read(value1)
        place2, transition2, incidenceMatrix2 = pnml_read.read(value2)

        val = model.compare.place_hungarian(place1, transition1, incidenceMatrix1, place2, transition2, incidenceMatrix2)

        val = "Model similarity:" + str(val)
        self.echo(val)

    def generateLog(self):
        value1, ok = QInputDialog.getText(self, "Generate Log", "Input WFnet:", QLineEdit.Normal, "PLEASE INPUT CONTENTS")
        value2, ok = QInputDialog.getText(self, "Generate Log", "Input Size:", QLineEdit.Normal, "PLEASE INPUT CONTENTS")
        logPath = value1.split('.')[0]+ '_log.txt'
        if not os.path.exists(value1):
            return
        place, transition, incidenceMatrix = pnml_read.read(value1)
        log = Log.generate.stochastic_generate(place, transition, incidenceMatrix, int(value2))
        with open(logPath, 'w') as f:
            for item in log:
                f.write(' '.join(item))
                f.write('\n')
        textEdit = textedit.TextEdit(logPath)

        exception = None
        fh = None
        try:
            fh = QFile(textEdit.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            textEdit.setPlainText(stream.readAll())
            textEdit.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

        self.tabWidget.addTab(textEdit, textEdit.windowTitle())
        self.tabWidget.setCurrentWidget(textEdit)


    def runLog(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        logName = QFileInfo(textEdit.filename).fileName().split('.')[0]
        exception = None
        try:
            x, y, z = model.alpha.get_incidenceMatrix(model.alpha.get_log(textEdit.filename))
            k = pnml_generate.PNML(logName, x, y, z)
            pnml_string = k.get_pnmlString()
            imgName = './output/' + logName
            logName = './output/' + logName + '.pnml'
            with open(logName, 'w') as pnml_file:
                pnml_file.write(pnml_string)
            pnml_show.show(logName, imgName)
        except EnvironmentError as e:
            exception = e
        finally:
            if exception is not None:
                raise exception

    def echo(self, value):
        '''显示对话框返回值'''
        QMessageBox.information(self, "Output", "{}".format(value),
                                QMessageBox.Yes | QMessageBox.No)

    def replaceContents(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        value1, ok = QInputDialog.getText(self, "Input", "Find Object:", QLineEdit.Normal, "PLEASE INPUT CONTENTS")
        if textEdit.toPlainText().count(value1):
            value2, ok = QInputDialog.getText(self, "Input", "Replace Object:", QLineEdit.Normal, "PLEASE INPUT CONTENTS")
            text = textEdit.toPlainText().replace(value1, value2)
            textEdit.clear()
            textEdit.insertPlainText(text)
            self.echo("Replace Successfully.")
        else:
            self.echo("No Match.")

    def findContents(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        value, ok = QInputDialog.getText(self, "Input", "Find Object:", QLineEdit.Normal, "PLEASE INPUT CONTENTS")
        self.echo(textEdit.toPlainText().count(value))


    def cutContents(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            cursor.removeSelectedText()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    def pasteFile(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        clipboard = QApplication.clipboard()
        textEdit.insertPlainText(clipboard.text())

    def copyFile(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    def closeTab(self):
        widget = self.tabWidget.currentWidget()
        if widget is None:
            return
        widget.close()
        self.tabWidget.removeTab(self.tabWidget.currentIndex())

    def saveasFile(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return True
        filename,filetype = QFileDialog.getSaveFileName(self,
                "PyProm - Save File As", textEdit.filename,
                "All types(*.*)")
        if filename:
            textEdit.filename = filename
            return self.saveFile()
        return True

    def saveFile(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return True
        try:
            textEdit.save()
            self.tabWidget.setTabText(self.tabWidget.currentIndex(),
                                      QFileInfo(textEdit.filename).fileName())
            self.listWidget.addItem(textEdit.filename+" Save Successfully.")
            return True
        except EnvironmentError as e:
            QMessageBox.warning(self,
                                "Tabbed Text Editor -- Save Error",
                                "Failed to save {0}: {1}".format(textEdit.filename, e))
            return False

    def newFile(self):
        textEdit = textedit.TextEdit()
        self.tabWidget.addTab(textEdit, textEdit.windowTitle())
        self.tabWidget.setCurrentWidget(textEdit)

    def showVersion(self):
        QMessageBox.information(self, "version", "Version 1.0")

    def openFolder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder", "./")
        if not os.path.exists(path):
            return
        self.treeWidget.clear()
        self.signal_dirpath.emit(path)

    def function(self, item, column):
        path = item.text(0)
        item = item.parent()
        while True:
            path = item.text(0) + '/' + path
            item = item.parent()
            if item is None:
                break
        if path.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff', '.ico')):

            graphicsView = QtWidgets.QGraphicsView()
            self.tabWidget.addTab(graphicsView, path.split('/')[-1])
            self.tabWidget.setCurrentWidget(graphicsView)

            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8),-1)  # 读取图像
            img = cv2.resize(img, (804,497))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道

            x = img.shape[1]  # 获取图像大小
            y = img.shape[0]
            frame = QImage(img, x, y, QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
            item = QGraphicsPixmapItem(pix)  # 创建像素图元
            scene = QGraphicsScene()  # 创建场景
            scene.addItem(item)
            graphicsView.setScene(scene)  # 将场景添加至视图
            graphicsView.show()
        else:
            textEdit = textedit.TextEdit(path)
            exception = None
            fh = None
            try:
                fh = QFile(textEdit.filename)
                if not fh.open(QIODevice.ReadOnly):
                    raise IOError(str(fh.errorString()))
                stream = QTextStream(fh)
                stream.setCodec("UTF-8")
                textEdit.setPlainText(stream.readAll())
                textEdit.document().setModified(False)
            except EnvironmentError as e:
                exception = e
            finally:
                if fh is not None:
                    fh.close()
                if exception is not None:
                    raise exception

            self.tabWidget.addTab(textEdit, textEdit.windowTitle())
            self.tabWidget.setCurrentWidget(textEdit)

    def showFolder(self, path):

        dirs = os.listdir(path)
        fileInfo = Qt.QFileInfo(path)
        fileIcon = Qt.QFileIconProvider()
        icon = QtGui.QIcon(fileIcon.icon(fileInfo))
        root = QTreeWidgetItem(self.treeWidget)
        root.setText(0, path)
        root.setIcon(0, QtGui.QIcon(icon))
        self.CreateTree(dirs, root, path)
        QApplication.processEvents()

    def CreateTree(self, dirs, root, path):
        for i in dirs:
            path_new = path + '\\' + i
            if os.path.isdir(path_new):
                fileInfo = Qt.QFileInfo(path_new)
                fileIcon = Qt.QFileIconProvider()
                icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QtGui.QIcon(icon))
                dirs_new = os.listdir(path_new)
                self.CreateTree(dirs_new, child, path_new)
            else:
                fileInfo = Qt.QFileInfo(path_new)
                fileIcon = Qt.QFileIconProvider()
                icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QtGui.QIcon(icon))

# root = QFileInfo(__file__).absolutePath()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
