import numpy as np

class Gomoku:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.current_player = 1  # 1表示黑子，2表示白子
        self.game_over = False
        self.winner = None
        self.history = []  # 用于记录游戏历史

    def make_move(self, row, col):
        """在指定位置落子"""
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.history.append((row, col, self.current_player))
            
            if self.check_win(row, col):
                self.game_over = True
                self.winner = self.current_player
                return True
                
            self.current_player = 3 - self.current_player  # 切换玩家
            return True
        return False

    def is_valid_move(self, row, col):
        """检查移动是否有效"""
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
        return self.board[row][col] == 0

    def check_win(self, row, col):
        """检查是否获胜"""
        player = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、主对角线、副对角线
        
        for dx, dy in directions:
            count = 1
            # 正向检查
            for i in range(1, 5):
                new_row, new_col = row + dx * i, col + dy * i
                if not self.is_in_board(new_row, new_col) or self.board[new_row][new_col] != player:
                    break
                count += 1
            # 反向检查
            for i in range(1, 5):
                new_row, new_col = row - dx * i, col - dy * i
                if not self.is_in_board(new_row, new_col) or self.board[new_row][new_col] != player:
                    break
                count += 1
            if count >= 5:
                return True
        return False

    def is_in_board(self, row, col):
        """检查坐标是否在棋盘内"""
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def undo_move(self):
        """撤销上一步移动"""
        if self.history:
            row, col, player = self.history.pop()
            self.board[row][col] = 0
            self.current_player = player
            self.game_over = False
            self.winner = None
            return True
        return False

    def get_board_state(self):
        """获取当前棋盘状态"""
        return self.board.copy()

    def display_board(self):
        """显示棋盘"""
        symbols = {0: '·', 1: '●', 2: '○'}
        # 打印列标号
        print('  ', end='')
        for i in range(self.board_size):
            print(f'{i:2}', end='')
        print()
        # 打印棋盘内容
        for i, row in enumerate(self.board):
            print(f'{i:2}', end='')
            for cell in row:
                print(f'{symbols[cell]} ', end='')
            print() 