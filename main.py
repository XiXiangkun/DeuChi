import sys
from PyQt6.QtWidgets import QApplication
from screen_mask import ScreenMask
from text_window import TextWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScreenMask()  # 主窗口
    translate_display = TextWindow()  # 文本翻译显示窗口
    translate_display.hide()
    window.show()
    window.show_translate.connect(translate_display.show_window)  # 隐藏主窗口，显示文本窗口
    window.text_translated.connect(translate_display.text_update)  # 文本刷新
    translate_display.translate_stop.connect(window.stop_translate)  # 停止翻译，隐藏文本窗口，显示主窗口
    translate_display.set_update_time.connect(window.change_update_time)
    sys.exit(app.exec())
