import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QHBoxLayout, QSlider, QGroupBox,
                           QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPixmap, QIcon
from gomoku import Gomoku
from sound_manager import SoundManager
import os

class GomokuBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.board_size = 15
        self.cell_size = 40
        self.margin = 30
        self.pieces = []  # 存储落子位置
        self.current_player = 1  # 1为黑子，2为白子
        self.game_over = False
        self.sound_manager = SoundManager()
        
        # 加载木纹背景
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.background = QPixmap(os.path.join(current_dir, "assets", "wood_texture.jpg"))
        
        # 设置固定大小
        board_width = self.board_size * self.cell_size + 2 * self.margin
        board_height = self.board_size * self.cell_size + 2 * self.margin
        self.setFixedSize(board_width, board_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制木纹背景
        painter.drawPixmap(self.rect(), self.background)

        # 绘制棋盘网格
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        painter.setPen(pen)

        # 绘制横线和竖线
        for i in range(self.board_size):
            # 横线
            painter.drawLine(
                self.margin, self.margin + i * self.cell_size,
                self.margin + (self.board_size - 1) * self.cell_size, self.margin + i * self.cell_size
            )
            # 竖线
            painter.drawLine(
                self.margin + i * self.cell_size, self.margin,
                self.margin + i * self.cell_size, self.margin + (self.board_size - 1) * self.cell_size
            )

        # 绘制天元和星位
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for x, y in star_points:
            center = QPoint(
                self.margin + x * self.cell_size,
                self.margin + y * self.cell_size
            )
            painter.setBrush(QBrush(Qt.black))
            painter.drawEllipse(center, 4, 4)

        # 绘制棋子
        for piece in self.pieces:
            x, y, player = piece
            center = QPoint(
                self.margin + x * self.cell_size,
                self.margin + y * self.cell_size
            )
            
            if player == 1:  # 黑子
                painter.setBrush(QBrush(Qt.black))
            else:  # 白子
                painter.setBrush(QBrush(Qt.white))
            
            painter.setPen(QPen(Qt.black))
            painter.drawEllipse(center, self.cell_size // 2 - 2, self.cell_size // 2 - 2)

    def mousePressEvent(self, event):
        if self.game_over:
            return

        # 获取点击位置
        pos = event.pos()
        x = round((pos.x() - self.margin) / self.cell_size)
        y = round((pos.y() - self.margin) / self.cell_size)

        # 检查是否在有效范围内
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            # 检查该位置是否已有棋子
            if not any(p[0] == x and p[1] == y for p in self.pieces):
                self.pieces.append((x, y, self.current_player))
                self.sound_manager.play('place')
                
                # 检查是否获胜
                if self.check_win(x, y):
                    self.game_over = True
                    self.sound_manager.play('win')
                else:
                    self.current_player = 3 - self.current_player  # 切换玩家
                
                self.update()

    def check_win(self, x, y):
        """检查是否获胜"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、右斜、左斜
        player = self.current_player
        
        for dx, dy in directions:
            count = 1  # 当前方向的连续棋子数
            
            # 正向检查
            for i in range(1, 5):
                new_x, new_y = x + i * dx, y + i * dy
                if not (0 <= new_x < self.board_size and 0 <= new_y < self.board_size):
                    break
                if not any(p[0] == new_x and p[1] == new_y for p in self.pieces):
                    break
                count += 1
            
            # 反向检查
            for i in range(1, 5):
                new_x, new_y = x - i * dx, y - i * dy
                if not (0 <= new_x < self.board_size and 0 <= new_y < self.board_size):
                    break
                if not any(p[0] == new_x and p[1] == new_y for p in self.pieces):
                    break
                count += 1
            
            if count >= 5:
                return True
        
        return False

    def undo_move(self):
        """悔棋"""
        if self.pieces and not self.game_over:
            self.pieces.pop()
            self.current_player = 3 - self.current_player  # 切换玩家
            self.sound_manager.play('undo')
            self.update()

    def restart_game(self):
        """重新开始游戏"""
        self.pieces = []
        self.current_player = 1
        self.game_over = False
        self.update()

class GomokuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('五子棋')
        self.setFixedSize(900, 750)  # 减小窗口大小
        
        # 创建棋盘
        self.board = GomokuBoard()
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(20, 10, 20, 20)  # 设置边距
        
        # 标题区域
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 10)
        
        # 主标题
        main_title = QLabel("GOMOKU")
        main_title.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #2c3e50;
                font-family: 'Arial Black', sans-serif;
            }
        """)
        main_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_layout.addWidget(main_title)
        
        # 副标题
        subtitle = QLabel("by pegasus studio 2025")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                font-family: 'Arial', sans-serif;
            }
        """)
        subtitle.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        title_layout.addWidget(subtitle)
        
        # 控制按钮
        toggle_button = QPushButton("▶")
        toggle_button.setFixedSize(30, 30)
        toggle_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 4px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        title_layout.addWidget(toggle_button)
        
        main_layout.addLayout(title_layout)
        
        # 添加棋盘
        main_layout.addWidget(self.board, alignment=Qt.AlignCenter)
        
        # 创建浮动控制面板
        self.control_panel = QWidget(self)
        self.control_panel.setWindowFlags(Qt.Popup)  # 设置为弹出窗口
        self.control_panel.setFixedWidth(250)
        
        control_layout = QVBoxLayout(self.control_panel)
        control_layout.setSpacing(10)
        control_layout.setContentsMargins(10, 10, 10, 10)
        
        # 音乐控制面板
        music_control_panel = QGroupBox("音乐控制")
        music_control_layout = QVBoxLayout()
        music_control_layout.setSpacing(5)
        
        self.sound_effect_btn = QPushButton("音效: 开")
        self.sound_effect_btn.setCheckable(True)
        self.sound_effect_btn.setChecked(True)
        self.sound_effect_btn.clicked.connect(self.toggle_sound_effects)
        music_control_layout.addWidget(self.sound_effect_btn)
        
        self.bgm_btn = QPushButton("背景音乐: 开")
        self.bgm_btn.setCheckable(True)
        self.bgm_btn.setChecked(True)
        self.bgm_btn.clicked.connect(self.toggle_background_music)
        music_control_layout.addWidget(self.bgm_btn)
        
        self.music_style_btn = QPushButton("音乐风格: 和平")
        self.music_style_btn.clicked.connect(self.switch_background_music)
        music_control_layout.addWidget(self.music_style_btn)
        
        music_control_panel.setLayout(music_control_layout)
        control_layout.addWidget(music_control_panel)
        
        # 音量控制面板
        volume_panel = QGroupBox("音量控制")
        volume_layout = QVBoxLayout()
        volume_layout.setSpacing(5)
        
        sound_volume_layout = QHBoxLayout()
        sound_volume_label = QLabel("音效音量:")
        self.sound_volume_slider = QSlider(Qt.Horizontal)
        self.sound_volume_slider.setRange(0, 100)
        self.sound_volume_slider.setValue(50)
        self.sound_volume_slider.valueChanged.connect(self.change_sound_volume)
        sound_volume_layout.addWidget(sound_volume_label)
        sound_volume_layout.addWidget(self.sound_volume_slider)
        volume_layout.addLayout(sound_volume_layout)
        
        bgm_volume_layout = QHBoxLayout()
        bgm_volume_label = QLabel("背景音乐音量:")
        self.bgm_volume_slider = QSlider(Qt.Horizontal)
        self.bgm_volume_slider.setRange(0, 100)
        self.bgm_volume_slider.setValue(50)
        self.bgm_volume_slider.valueChanged.connect(self.change_bgm_volume)
        bgm_volume_layout.addWidget(bgm_volume_label)
        bgm_volume_layout.addWidget(self.bgm_volume_slider)
        volume_layout.addLayout(bgm_volume_layout)
        
        volume_panel.setLayout(volume_layout)
        control_layout.addWidget(volume_panel)
        
        # 游戏控制面板
        game_control_panel = QGroupBox("游戏控制")
        game_control_layout = QVBoxLayout()
        game_control_layout.setSpacing(5)
        
        undo_btn = QPushButton("悔棋")
        undo_btn.clicked.connect(self.board.undo_move)
        game_control_layout.addWidget(undo_btn)
        
        restart_btn = QPushButton("重新开始")
        restart_btn.clicked.connect(self.board.restart_game)
        game_control_layout.addWidget(restart_btn)
        
        game_control_panel.setLayout(game_control_layout)
        control_layout.addWidget(game_control_panel)
        
        # 设置控制面板样式
        self.control_panel.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border: none;
                border-radius: 8px;
            }
            QGroupBox {
                font-weight: bold;
                color: white;
                border: 1px solid #34495e;
                border-radius: 6px;
                margin-top: 15px;
                padding: 15px;
                background-color: #34495e;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #ecf0f1;
                background-color: #34495e;
            }
            QPushButton {
                padding: 8px;
                border: none;
                border-radius: 4px;
                background-color: #3498db;
                color: white;
                font-weight: bold;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:checked {
                background-color: #e74c3c;
            }
            QPushButton:checked:hover {
                background-color: #c0392b;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 12px;
            }
            QSlider {
                height: 20px;
            }
            QSlider::groove:horizontal {
                border: none;
                height: 4px;
                background: #7f8c8d;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: none;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #2980b9;
            }
        """)
        
        # 连接控制按钮
        toggle_button.clicked.connect(self.toggle_control_panel)
        
        # 设置主布局
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # 初始化音量设置
        self.board.sound_manager.set_volume(0.5)
        self.board.sound_manager.set_background_music_volume(0.5)

    def center_window(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def update_status(self, message):
        self.status_label.setText(message)

    def toggle_sound_effects(self):
        enabled = self.sound_effect_btn.isChecked()
        self.board.sound_manager.toggle()
        self.sound_effect_btn.setText(f"音效: {'开' if enabled else '关'}")

    def toggle_background_music(self):
        enabled = self.bgm_btn.isChecked()
        self.board.sound_manager.toggle_background_music()
        self.bgm_btn.setText(f"背景音乐: {'开' if enabled else '关'}")

    def switch_background_music(self):
        style_names = {
            'peaceful': '和平',
            'energetic': '活力',
            'mysterious': '神秘',
            'meditative': '冥想',
            'epic': '史诗',
            'jazz': '爵士'
        }
        current_style = self.board.sound_manager.switch_background_music()
        self.music_style_btn.setText(f"音乐风格: {style_names[current_style]}")

    def change_sound_volume(self, value):
        volume = value / 100.0
        self.board.sound_manager.set_volume(volume)

    def change_bgm_volume(self, value):
        volume = value / 100.0
        self.board.sound_manager.set_background_music_volume(volume)

    def toggle_control_panel(self):
        """显示/隐藏控制面板"""
        if self.control_panel.isVisible():
            self.control_panel.hide()
        else:
            # 计算控制面板的位置（在按钮右侧）
            button = self.sender()
            pos = button.mapToGlobal(button.rect().topRight())
            self.control_panel.move(pos.x() + 5, pos.y())
            # 添加阴影效果
            shadow = QGraphicsDropShadowEffect(self.control_panel)
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 80))
            shadow.setOffset(0, 0)
            self.control_panel.setGraphicsEffect(shadow)
            self.control_panel.show()

    def closeEvent(self, event):
        self.board.sound_manager.cleanup()
        event.accept()

def main():
    print("正在初始化应用程序...")
    app = QApplication(sys.argv)
    print("正在创建主窗口...")
    window = GomokuWindow()
    print("正在显示窗口...")
    window.show()
    window.raise_()
    window.activateWindow()
    print("进入主事件循环...")
    sys.exit(app.exec_())

if __name__ == '__main__':
    print("程序开始执行...")
    main() 