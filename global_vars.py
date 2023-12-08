class GlobalVariables:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 透明区域外部框在layout中坐标，以及对应MAC屏幕的真实坐标
        self.transparent_frame_x_real: int = 0
        self.transparent_frame_y_real: int = 0
        self.transparent_frame_width_real: int = 0
        self.transparent_frame_height_real: int = 0
        # 坐标不一致，所以多用了一组变量用来保存
        self.transparent_frame_x: int = 0
        self.transparent_frame_y: int = 0
        self.transparent_frame_width: int = 0
        self.transparent_frame_height: int = 0
        # 透明区域在layout中坐标，以及对应MAC屏幕的真实坐标
        self.transparent_x_real: int = 0
        self.transparent_y_real: int = 0
        self.transparent_width_real: int = 0
        self.transparent_height_real: int = 0
        # 坐标不一致，所以多用了一组变量用来保存
        self.transparent_x: int = 0
        self.transparent_y: int = 0
        self.transparent_width: int = 0
        self.transparent_height: int = 0

    def change_default(self, transparent_frame_x_real, transparent_frame_y_real,
                       transparent_frame_width_real, transparent_frame_height_real):
        self.transparent_frame_x_real = transparent_frame_x_real
        self.transparent_frame_y_real = transparent_frame_y_real
        self.transparent_frame_width_real = transparent_frame_width_real
        self.transparent_frame_height_real = transparent_frame_height_real
        # 适配Mac Air做的调整，12为偏移数值
        # 适配Mac Air做的调整，99为37 + 40 + 10 + 12
        self.transparent_frame_x = self.transparent_frame_x_real - 12
        self.transparent_frame_y = self.transparent_frame_y_real - 99
        self.transparent_frame_width = self.transparent_frame_width_real
        self.transparent_frame_height = self.transparent_frame_height_real
        # 预留空闲边界位置
        self.transparent_x_real = self.transparent_frame_x_real + 4
        self.transparent_y_real = self.transparent_frame_y_real + 4
        self.transparent_width_real = self.transparent_frame_width_real - 8
        self.transparent_height_real = self.transparent_frame_height_real - 8
        # 对应真实坐标为 + 37 = 465，37固定是MAC菜单栏的高度
        self.transparent_x = self.transparent_x_real
        self.transparent_y = self.transparent_y_real - 37
        self.transparent_width = self.transparent_width_real
        self.transparent_height = self.transparent_height_real
