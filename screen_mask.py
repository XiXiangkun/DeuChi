import cv2
import time
import numpy as np
import threading
import pyautogui
import pytesseract
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QWidget, QComboBox, QPushButton
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtGui import QPainter
from googletrans import Translator
from global_vars import GlobalVariables
from transparent_frame import TransparentFrame


# 最底层Mask，通过paintEvent设置透明区域
class ScreenMask(QMainWindow):
    text_translated = pyqtSignal(str)
    show_translate = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.local_languages = []
        self.source_languange = "eng"
        self.time_interval = 2
        self.combobox_source = QComboBox()
        self.get_languages()
        self.layout_window = QVBoxLayout()
        # self.layout_window.setContentsMargins(0, 0, 0, 0)
        self.layout_button = QHBoxLayout()
        self.layout_button.setContentsMargins(0, 0, 0, 0)
        self.layout_screen = QVBoxLayout()
        self.layout_screen.setContentsMargins(0, 0, 0, 0)
        self.set_window_geometry()
        self.set_window_layout()
        self.painter_init = 0
        self.global_instance = GlobalVariables()
        self.translator = Translator()
        self.global_instance.change_default(481, 461, 508, 208)  # 自定义的Mac Air2初始化位置
        self.translate_flag = False

    # 设置Mask大小，默认不包含菜单栏，所以height-37
    def set_window_geometry(self):
        screen_geo_wid, screen_geo_av_hei = \
            QApplication.primaryScreen().geometry().width(), QApplication.primaryScreen().geometry().height() - 37
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        self.setGeometry(QApplication.primaryScreen().availableGeometry().x(),
                         QApplication.primaryScreen().availableGeometry().y(),
                         screen_geo_wid, screen_geo_av_hei)

    # Mask分为两部分，上部分buttons，下部分screen
    def set_window_layout(self):
        self.set_options()
        self.set_frame()
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: transparent")
        central_widget.setLayout(self.layout_window)
        self.setCentralWidget(central_widget)

    # 设置buttons部分，高度指定为40，通过set_label_style和set_combobox_style函数设置buttons
    def set_options(self):
        layout_button_widget = QWidget()
        layout_button_widget.setMaximumHeight(40)
        layout_button_widget.setLayout(self.layout_button)
        space_item_start = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        space_item_end = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        label_source = QLabel("源语言: ")
        label_translate = QLabel("————>")
        label_target = QLabel("目标语言: 中文")

        run_button = QPushButton("Run")
        self.set_label_style(label_source)
        self.set_label_style(label_translate)
        self.set_label_style(label_target)
        self.set_combobox_item(self.combobox_source)
        self.set_button_style(run_button)
        run_button.clicked.connect(self.run_button_clicked)
        self.layout_button.addSpacerItem(space_item_start)
        self.layout_button.addWidget(label_source)
        self.layout_button.addWidget(self.combobox_source)
        self.layout_button.addWidget(label_translate)
        self.layout_button.addWidget(label_target)
        self.layout_button.addWidget(run_button)
        self.layout_button.addSpacerItem(space_item_end)
        self.layout_window.addWidget(layout_button_widget)

    # 设置screen部分，透明区域的边缘窗口
    def set_frame(self):
        layout_screen_widget = QWidget()
        tmp_frame = TransparentFrame()
        tmp_frame.setMinimumSize(10, 10)  # 防止窗口太小导致不可见
        tmp_frame.transparent_window_changed.connect(self.repaint_window)
        space_item_start = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        space_item_end = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        layout_screen_widget.setLayout(self.layout_screen)
        self.layout_screen.addSpacerItem(space_item_start)
        self.layout_screen.addWidget(tmp_frame)
        self.layout_screen.addSpacerItem(space_item_end)
        self.layout_window.addWidget(layout_screen_widget)

    @staticmethod
    def set_label_style(tmp_label):
        tmp_label.setFixedWidth(110)
        tmp_label.setStyleSheet("color: #53c6c6; font-size: 16px")
        tmp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # @staticmethod
    def set_combobox_item(self, tmp_combobox):
        tmp_combobox.setMinimumHeight(28)
        tmp_combobox.setFixedWidth(130)
        tmp_combobox.view().setMinimumWidth(tmp_combobox.width())
        tmp_font = tmp_combobox.font()
        tmp_font.setPointSize(16)
        tmp_combobox.setFont(tmp_font)
        tmp_combobox.setStyleSheet(
            "QComboBox { color: #53c6c6; background-color: rgba(0, 0, 0, 15)}"
            "QComboBox { border: 1px solid #53c6c6; border-radius: 5px; padding: 4px}"
        )
        for lan in self.local_languages:
            tmp_combobox.addItem(lan)

    @staticmethod
    def set_button_style(tmp_button):
        tmp_button.setMinimumSize(80, 25)
        tmp_button.setStyleSheet(
            "QPushButton { color: #f6fcfc; border: 1px solid #53c6c6;}"
            "QPushButton { font-size: 16px; border-radius: 5px; min-height: 28px;}"
            "QPushButton:hover { color: #53c6c6;}"
            "QPushButton:pressed { color: #206060;}"
        )

    # 初始化设置默认的透明区域
    def paintEvent(self, event):
        painter = QPainter(self)
        transparent_region = self.rect().intersected(
            QRect(
                self.global_instance.transparent_x, self.global_instance.transparent_y,
                self.global_instance.transparent_width, self.global_instance.transparent_height
            )
        )
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.fillRect(transparent_region, Qt.GlobalColor.transparent)

    # 重新绘制透明区域
    def repaint_window(self, *args):
        tmp_x, tmp_y, tmp_width, tmp_height = args
        self.global_instance.change_default(tmp_x, tmp_y, tmp_width, tmp_height)
        self.update()

    # Run按键按下后的逻辑
    def run_button_clicked(self):
        self.source_languange = self.combobox_source.currentText()
        self.hide()
        self.show_translate.emit()
        self.translate_flag = True
        translate_thread = threading.Thread(target=self.run_translate)
        translate_thread.start()

    # 开启线程，执行翻译，两秒一次
    def run_translate(self):
        while self.translate_flag:
            self.process_image(self.capture_screen())
            time.sleep(self.time_interval)

    # 获取Rect内的图片
    def capture_screen(self):
        tmp_screenshot = pyautogui.screenshot(
            region=(self.global_instance.transparent_x_real,
                    self.global_instance.transparent_y_real,
                    self.global_instance.transparent_width_real,
                    self.global_instance.transparent_height_real))
        return tmp_screenshot

    # 图片识别，转文本翻译
    def process_image(self, capture_image):
        image = np.array(capture_image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        try:
            origin_text = pytesseract.image_to_string(image_gray, lang=self.source_languange)
            origin_text = origin_text.replace("\n", " ")
        except Exception:
            origin_text = "Something wrong... Seems like this Traineddata is not founded in Pytesseract"
            origin_text = origin_text.replace("\n", " ")
        try:
            real_translation = self.translator.translate(origin_text, dest='zh-CN')
            self.text_translated.emit(real_translation.text)
        except ConnectionError:
            self.text_translated.emit("ConnectionError of Googletrans")
        except Exception:
            self.text_translated.emit("Something wrong with Googletrans")

    # 停止翻译
    def stop_translate(self):
        self.translate_flag = False
        self.show()

    def get_languages(self):
        self.local_languages = pytesseract.get_languages()
        self.local_languages.remove("osd")
        self.local_languages.remove("snum")

    def change_update_time(self, num):
        self.time_interval = num
