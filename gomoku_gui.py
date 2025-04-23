import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPixmap
from gomoku import Gomoku
import os

class GomokuBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.game = Gomoku()
        self.cell_size = 40
        self.margin = 40
        self.stone_size = 36
        self.main_window = parent
        
        # 加载木纹背景
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.background = QPixmap(os.path.join(current_dir, "assets", "wood_texture.jpg"))
        
        # 设置固定大小
        board_size = (self.cell_size * 14 + self.margin * 2)
        self.setFixedSize(board_size, board_size)
        
        self.setMouseTracking(True)
        self.hover_pos = None

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
        for i in range(15):
            # 横线
            painter.drawLine(
                self.margin, self.margin + i * self.cell_size,
                self.margin + 14 * self.cell_size, self.margin + i * self.cell_size
            )
            # 竖线
            painter.drawLine(
                self.margin + i * self.cell_size, self.margin,
                self.margin + i * self.cell_size, self.margin + 14 * self.cell_size
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
        for i in range(15):
            for j in range(15):
                if self.game.board[i][j] != 0:
                    self.draw_stone(painter, i, j, self.game.board[i][j])

        # 绘制悬停提示
        if self.hover_pos and not self.game.game_over:
            row, col = self.hover_pos
            if self.game.is_valid_move(row, col):
                self.draw_stone(painter, row, col, self.game.current_player, 0.5)

    def draw_stone(self, painter, row, col, stone_type, opacity=1.0):
        center = QPoint(
            self.margin + col * self.cell_size,
            self.margin + row * self.cell_size
        )
        
        if opacity < 1.0:
            painter.setOpacity(opacity)
            
        if stone_type == 1:  # 黑子
            painter.setBrush(QBrush(Qt.black))
            painter.setPen(QPen(Qt.black))
        else:  # 白子
            painter.setBrush(QBrush(Qt.white))
            painter.setPen(QPen(Qt.black))
            
        painter.drawEllipse(center, self.stone_size // 2, self.stone_size // 2)
        painter.setOpacity(1.0)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        x = round((pos.x() - self.margin) / self.cell_size)
        y = round((pos.y() - self.margin) / self.cell_size)
        
        if 0 <= x < 15 and 0 <= y < 15:
            self.hover_pos = (y, x)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and not self.game.game_over:
            pos = event.pos()
            col = round((pos.x() - self.margin) / self.cell_size)
            row = round((pos.y() - self.margin) / self.cell_size)
            
            if 0 <= col < 15 and 0 <= row < 15:
                if self.game.make_move(row, col):
                    self.update()
                    if self.game.game_over:
                        winner = "黑方" if self.game.winner == 1 else "白方"
                        self.main_window.update_status(f"游戏结束！{winner}获胜！")
                    else:
                        current = "黑方" if self.game.current_player == 1 else "白方"
                        self.main_window.update_status(f"当前回合：{current}")

class GomokuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("五子棋")
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建垂直布局
        layout = QVBoxLayout(main_widget)
        
        # 创建状态标签
        self.status_label = QLabel("当前回合：黑方")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 创建棋盘
        self.board = GomokuBoard(self)
        layout.addWidget(self.board)
        
        # 创建控制按钮
        button_layout = QVBoxLayout()
        
        undo_button = QPushButton("撤销")
        undo_button.clicked.connect(self.undo_move)
        button_layout.addWidget(undo_button)
        
        new_game_button = QPushButton("新游戏")
        new_game_button.clicked.connect(self.new_game)
        button_layout.addWidget(new_game_button)
        
        layout.addLayout(button_layout)
        
        # 设置窗口大小和位置
        self.setFixedSize(layout.sizeHint())
        self.center_window()

    def center_window(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def update_status(self, message):
        self.status_label.setText(message)

    def undo_move(self):
        if self.board.game.undo_move():
            self.board.update()
            current = "黑方" if self.board.game.current_player == 1 else "白方"
            self.update_status(f"当前回合：{current}")

    def new_game(self):
        self.board.game = Gomoku()
        self.board.update()
        self.update_status("当前回合：黑方")

def main():
    app = QApplication(sys.argv)
    window = GomokuWindow()
    window.show()
    sys.exit(app.exec_()) 