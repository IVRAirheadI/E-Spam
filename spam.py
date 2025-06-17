import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont

import keyboard

class SpammerThread(QThread):
    status_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._interval = 0.03

    def run(self):
        while True:
            if self._running:
                keyboard.send('e')
            time.sleep(self._interval)

    def toggle_spam(self):
        self._running = not self._running
        self.status_signal.emit(self._running)

    @property
    def is_running(self):
        return self._running

class SpammerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_spam_thread()
        self.apply_cheat_aesthetic()
        self.setup_hotkey()

    def init_ui(self):
        self.setWindowTitle("Spam Tool")
        self.setGeometry(100, 100, 350, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        self.btn_toggle = QPushButton("START SPAMMING")
        self.btn_toggle.setFixedSize(250, 60)
        self.btn_toggle.clicked.connect(self.toggle_spam)
        layout.addWidget(self.btn_toggle, alignment=Qt.AlignCenter)

        self.lbl_info = QLabel("PRESS F7 TO TOGGLE SPAMMING (GLOBAL HOTKEY)")
        layout.addWidget(self.lbl_info, alignment=Qt.AlignCenter)

        self.message_box = QLabel(self)
        self.message_box.setAlignment(Qt.AlignCenter)
        self.message_box.setWordWrap(True)
        self.message_box.setStyleSheet("""
            color: #FFFF00;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 8px;
            border-radius: 5px;
            font-family: 'Consolas', 'Monospace', monospace;
            font-size: 13px;
            border: 1px solid #FFFF00;
        """)
        self.message_box.hide()
        layout.addWidget(self.message_box, alignment=Qt.AlignCenter)

    def init_spam_thread(self):
        self.spammer_thread = SpammerThread()
        self.spammer_thread.status_signal.connect(self.update_ui_state)
        self.spammer_thread.start()

    def toggle_spam(self):
        self.spammer_thread.toggle_spam()

    def update_ui_state(self, is_running):
        if is_running:
            self.btn_toggle.setText("STOP SPAMMING")
            self.btn_toggle.setStyleSheet(self.get_button_style(True))
            self.show_message("SPAMMING 'E' IS NOW ACTIVE!", 2000)
        else:
            self.btn_toggle.setText("START SPAMMING")
            self.btn_toggle.setStyleSheet(self.get_button_style(False))
            self.show_message("SPAMMING 'E' IS NOW INACTIVE.", 2000)

    def apply_cheat_aesthetic(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                border: 2px solid #00ff00;
                border-radius: 10px;
            }
            QLabel {
                color: #00ff00;
                font-family: 'Consolas', 'Monospace', monospace;
                font-size: 14px;
                padding: 5px;
            }
        """)

        font = QFont('Consolas', 12)
        self.lbl_info.setFont(font)
        self.lbl_info.setStyleSheet("color: #aaaaaa;")

        self.btn_toggle.setStyleSheet(self.get_button_style(False))

    def get_button_style(self, active):
        if active:
            return """
                QPushButton {
                    background-color: #006600;
                    color: #ffffff;
                    border: 2px solid #00ff00;
                    border-radius: 10px;
                    font-family: 'Consolas', 'Monospace', monospace;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 12px 25px;
                    box-shadow: 0 0 15px #00ff00;
                }
                QPushButton:hover {
                    background-color: #008800;
                    border: 2px solid #00ffff;
                    color: #ffffff;
                }
                QPushButton:pressed {
                    background-color: #003300;
                    border: 2px solid #00cc00;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #333333;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    border-radius: 8px;
                    font-family: 'Consolas', 'Monospace', monospace;
                    font-size: 16px;
                    padding: 10px 20px;
                    outline: none;
                }
                QPushButton:hover {
                    background-color: #444444;
                    border: 1px solid #00ffff;
                    color: #00ffff;
                }
                QPushButton:pressed {
                    background-color: #004d00;
                    border: 1px solid #00ff00;
                }
            """

    def setup_hotkey(self):
        def hotkey_callback():
            self.toggle_spam()
        keyboard.add_hotkey('f7', hotkey_callback)

    def show_message(self, message, duration_ms=1500):
        self.message_box.setText(message)
        self.message_box.adjustSize()
        self.message_box.move(
            int((self.width() - self.message_box.width()) / 2),
            int(self.height() - self.message_box.height() - 15)
        )
        self.message_box.show()
        QTimer.singleShot(duration_ms, self.message_box.hide)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SpammerApp()
    ex.show()
    sys.exit(app.exec_())
