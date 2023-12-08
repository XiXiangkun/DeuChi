from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QAbstractSpinBox, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal


class TextWindow(QWidget):
    translate_stop = pyqtSignal()
    set_update_time = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 150)
        self.move(1000, 150)

        self.speed_value = 2
        speed_options_layout = QHBoxLayout()
        minus_button = QPushButton("-")
        self.num_label = QPushButton("Speed x 2.0")
        plus_button = QPushButton("+")
        back_button = QPushButton("Back to Options")
        self.text_label = QLabel("Translated output is here...")
        minus_button.clicked.connect(self.minus_speed)
        plus_button.clicked.connect(self.plus_speed)
        back_button.clicked.connect(self.back_window)
        self.set_plus_button_style(minus_button)
        self.set_button_style(self.num_label)
        self.set_plus_button_style(plus_button)
        self.set_button_style(back_button)
        self.set_label_style(self.text_label)
        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)
        speed_options_layout.setContentsMargins(0, 0, 0, 0)
        speed_options_layout.addWidget(minus_button)
        speed_options_layout.addWidget(self.num_label)
        speed_options_layout.addWidget(plus_button)
        speed_options_layout.addWidget(back_button)
        layout.addLayout(speed_options_layout)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

    def set_text(self, text):
        self.text_label.setText(text)

    @staticmethod
    def set_plus_button_style(tmp_button):
        tmp_button.setStyleSheet(
            "QPushButton { background-color: rgba(0, 0, 0, 10); color: #39acac; font-size: 16px; max-width: 30px;}"
            "QPushButton:hover { color: #339999;}"
            "QPushButton:pressed { color: #339999; border: 1px solid #339999}"
        )

    @staticmethod
    def set_button_style(tmp_button):
        tmp_button.setStyleSheet(
            "QPushButton { background-color: rgba(0, 0, 0, 10); color: #2d8686; font-size: 16px;}"
            "QPushButton:hover { color: #339999;}"
            "QPushButton:pressed { color: #339999; border: 1px solid #339999}"
        )

    @staticmethod
    def set_label_style(tmp_label):
        tmp_label.resize(400, 150)
        tmp_label.setWordWrap(True)
        tmp_label.setStyleSheet("background-color: rgba(0, 0, 0, 10); color: #339999; "
                                "font-size: 16px; padding: 2px;")
        tmp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def text_update(self, text):
        self.text_label.setText(text)

    def show_window(self):
        self.show()

    def back_window(self):
        self.hide()
        self.translate_stop.emit()

    def minus_speed(self):
        if self.speed_value == 0.5:
            pass
        else:
            self.speed_value -= 0.5
            button_text = "Speed x " + str(self.speed_value)
            self.num_label.setText(button_text)
            print(self.speed_value)

    def plus_speed(self):
        self.speed_value += 0.5
        button_text = "Speed x " + str(self.speed_value)
        self.num_label.setText(button_text)
        print(self.speed_value)

    def spinbox_value_changed(self):
        pass
