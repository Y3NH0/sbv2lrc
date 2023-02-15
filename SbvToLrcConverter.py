from utils import sbv2lrc
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QPlainTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

class SbvToLrcConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        # init the title & window size of the applciation
        self.setWindowTitle('SBV to LRC Converter')
        self.setGeometry(100, 100, 600, 600)

        # construct all the object in this app
        self.input_text = QPlainTextEdit(self)
        self.input_text.setAcceptDrops(True)

        self.output_text = QPlainTextEdit(self)
        self.output_text.setReadOnly(True)

        self.input_label = QLabel('paste the sbv context or drag the .sbv file', self)
        self.output_label = QLabel('lrc', self)

        self.convert_button = QPushButton('Convert', self)
        self.export_button = QPushButton('Export', self)

        # connect the 'drag and drop' event to self.input_text
        self.input_text.dragEnterEvent = self.drag_enter_event
        self.input_text.dropEvent = self.drop_event

        # connect the click event to the buttons
        self.convert_button.clicked.connect(self.convert_sbv_to_lrc)
        self.export_button.clicked.connect(self.export_lrc_file)

        # layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.input_label)
        vbox.addWidget(self.input_text)
        vbox.addWidget(self.convert_button)
        vbox.addWidget(self.output_label)
        vbox.addWidget(self.output_text)
        vbox.addWidget(self.export_button)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def drag_enter_event(self, event):
        # any file be dragged ?
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        # read file
        file_path = event.mimeData().urls()[0].toLocalFile()
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # drop the content in the block(self.input_text)
        self.input_text.setPlainText(content)

    def convert_sbv_to_lrc(self):
        # read self.input_text
        sbv_content = self.input_text.toPlainText()

        # if no input
        if sbv_content.strip() == '':
            QMessageBox.warning(self, 'WARNING', 'UR INPUT ????')
            return
        
        # convert
        lrc = sbv2lrc(sbv_content)

        # output the result
        self.output_text.setPlainText(lrc)

    def export_lrc_file(self):
        # let user specify the path to export_file
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save', '', 'LRC Files (*.lrc)')

        # if not
        if not file_path:
            return

        # write file
        with open(file_path, 'w', encoding='utf-8') as lrc_file:
            lrc_file.writelines(self.output_text.toPlainText())
        
if __name__ == '__main__':
    app = QApplication([])
    sbv_to_lrc_converter = SbvToLrcConverter()
    app.exec_()
