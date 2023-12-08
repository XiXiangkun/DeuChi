from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from global_vars import GlobalVariables


# 模拟透明窗口的边缘效果，使用QFrame窗口实现
class TransparentFrame(QFrame):
    transparent_window_changed = pyqtSignal(int, int, int, int)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: transparent; border: 2px dashed #339999")
        self.setMouseTracking(True)
        self.offset = QPoint()
        self.transparent_inside_dragging = False
        self.transparent_border_dragging = False
        self.drag_start_position = QPoint()
        self.frame_geometry = None
        self.painter_init = 0
        self.which_border = None  # top=0, bottom=1, left=2, right=3
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.global_instance = GlobalVariables()
        self.old_transparent_frame_x_real, self.old_transparent_frame_y_real = \
            self.global_instance.transparent_frame_x_real, self.global_instance.transparent_frame_y_real
        self.offset_x, self.offset_y = 0, 0

    # 鼠标左键按下，判断是拉伸还是移动
    def mousePressEvent(self, event):
        self.old_transparent_frame_x_real, self.old_transparent_frame_y_real = \
            self.global_instance.transparent_frame_x_real, self.global_instance.transparent_frame_y_real
        if event.button() & Qt.MouseButton.LeftButton:
            if self.which_border is not None:
                self.transparent_border_dragging = True
            else:
                self.transparent_inside_dragging = True
            self.drag_start_position = event.globalPosition()
            self.frame_geometry = self.geometry()

    # 鼠标按住移动，进行放缩、移动调整；
    # 鼠标正常移动，在窗口边缘变换鼠标UI
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            offset = event.globalPosition() - self.drag_start_position
            if abs(offset.x()) > 1 or abs(offset.y()) > 1:
                self.resize_or_move(offset)
        else:
            if self.global_instance.transparent_x_real - 2 <= event.globalPosition().x() \
                    <= self.global_instance.transparent_x_real + 2:
                self.which_border = 2
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            elif self.global_instance.transparent_x_real + \
                    self.global_instance.transparent_width_real - 2 <= event.globalPosition().x():
                self.which_border = 3
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            elif self.global_instance.transparent_y_real - 2 <= \
                    event.globalPosition().y() <= self.global_instance.transparent_y_real + 2:
                self.which_border = 0
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            elif self.global_instance.transparent_y_real + \
                    self.global_instance.transparent_height_real - 2 <= event.globalPosition().y() <= \
                    self.global_instance.transparent_y_real + \
                    self.global_instance.transparent_height_real + 2:
                self.which_border = 1
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            else:
                self.which_border = None
                self.setCursor(Qt.CursorShape.ArrowCursor)

    # 调整或移动QFrame窗口
    def resize_or_move(self, offset):
        self.offset_x = int(offset.x())
        self.offset_y = int(offset.y())
        if self.transparent_border_dragging:
            if self.which_border == 0:
                self.offset_x = 0
                if self.global_instance.transparent_frame_height_real - self.offset_y <= 50:
                    self.offset_y = self.global_instance.transparent_frame_height_real - 50
                self.resize(self.global_instance.transparent_frame_width_real,
                            self.global_instance.transparent_frame_height_real - self.offset_y)
                self.move(self.global_instance.transparent_frame_x,
                          self.global_instance.transparent_frame_y + self.offset_y)
            elif self.which_border == 1:
                self.offset_x = 0
                if self.global_instance.transparent_frame_height_real + self.offset_y <= 50:
                    self.offset_y = -(self.global_instance.transparent_frame_height_real - 50)
                self.resize(self.global_instance.transparent_frame_width_real,
                            self.global_instance.transparent_frame_height_real + self.offset_y)
            elif self.which_border == 2:
                self.offset_y = 0
                if self.global_instance.transparent_frame_width_real - self.offset_x <= 100:
                    self.offset_x = self.global_instance.transparent_frame_width_real - 100
                self.resize(self.global_instance.transparent_frame_width_real - self.offset_x,
                            self.global_instance.transparent_frame_height_real)
                self.move(self.global_instance.transparent_frame_x + self.offset_x,
                          self.global_instance.transparent_frame_y)
            elif self.which_border == 3:
                self.offset_y = 0
                if self.global_instance.transparent_frame_width_real + self.offset_x <= 100:
                    self.offset_x = -(self.global_instance.transparent_frame_width_real - 100)
                self.resize(self.global_instance.transparent_frame_width_real + self.offset_x,
                            self.global_instance.transparent_frame_height_real)
            else:
                pass
        else:
            self.move(self.frame_geometry.topLeft() + QPoint(int(offset.x()), int(offset.y())))
            self.transparent_window_changed.emit(self.frame_geometry.topLeft().x() + int(offset.x()) + 12,
                                                 self.frame_geometry.topLeft().y() + int(offset.y()) + 99,
                                                 self.global_instance.transparent_frame_width_real,
                                                 self.global_instance.transparent_frame_height_real)

    # 鼠标释放，恢复鼠标UI
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.transparent_border_dragging:
                if self.which_border == 0 or self.which_border == 2:
                    self.transparent_window_changed.emit(self.old_transparent_frame_x_real + self.offset_x,
                                                         self.old_transparent_frame_y_real + self.offset_y,
                                                         self.global_instance.transparent_frame_width_real -
                                                         self.offset_x,
                                                         self.global_instance.transparent_frame_height_real -
                                                         self.offset_y)
                elif self.which_border == 1 or self.which_border == 3:
                    self.transparent_window_changed.emit(self.old_transparent_frame_x_real,
                                                         self.old_transparent_frame_y_real,
                                                         self.global_instance.transparent_frame_width_real +
                                                         self.offset_x,
                                                         self.global_instance.transparent_frame_height_real +
                                                         self.offset_y)
            self.transparent_inside_dragging = False
            self.transparent_border_dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        self.offset_x = 0
        self.offset_y = 0

    # 设置初始状态下的QFrame窗口位置、大小
    def paintEvent(self, event):
        if self.painter_init == 0:
            self.setGeometry(self.global_instance.transparent_frame_x,
                             self.global_instance.transparent_frame_y,
                             self.global_instance.transparent_frame_width,
                             self.global_instance.transparent_frame_height)
            self.painter_init = 1
