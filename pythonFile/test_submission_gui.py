import sys
from PyQt5.QtWidgets import *

class DropWidget(QWidget):
    def __init__(self, parent=None):
        super(DropWidget, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()
        mimeData = event.mimeData()
        print('dragEnterEvent')
        for mimetype in mimeData.formats():
            print('MIMEType:', mimetype)
            print('Data:', mimeData.data)
            print()
        print()

    def dropEvent(self, event):
        event.accept()
        mimeData = event.mimeData()
        print('dropEvent')
        for mimetype in mimeData.formats():
            print('MIMEType:', mimetype)
            print('Data:', mimeData.data(mimetype))
            print()
        print()

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ラベル名の設定
        lbl1 = QLabel('Drag and drop the submission.csv', self)
        # ラベルをx=15,y=10へ移動
        lbl1.move(15, 10)
        w = DropWidget(self)
        w.resize(300, 300)
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Calculate Submission')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
