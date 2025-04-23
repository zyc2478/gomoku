import pytest
from gomoku import Gomoku

def test_initialization():
    """测试游戏初始化"""
    game = Gomoku()
    assert game.board_size == 15
    assert game.current_player == 1
    assert not game.game_over
    assert game.winner is None
    assert len(game.history) == 0

def test_valid_move():
    """测试有效移动"""
    game = Gomoku()
    assert game.make_move(7, 7)
    assert game.board[7][7] == 1
    assert game.current_player == 2
    assert len(game.history) == 1

def test_invalid_move():
    """测试无效移动"""
    game = Gomoku()
    # 测试已占用位置
    game.make_move(7, 7)
    assert not game.make_move(7, 7)
    assert game.current_player == 2
    
    # 测试超出边界的位置
    assert not game.make_move(-1, 7)
    assert not game.make_move(15, 7)
    assert not game.make_move(7, -1)
    assert not game.make_move(7, 15)

def test_win_horizontal():
    """测试水平方向获胜"""
    game = Gomoku()
    # 黑棋横向五子
    for col in range(5):
        game.make_move(7, col)  # 黑棋
        if col < 4:
            game.make_move(8, col)  # 白棋
    
    assert game.game_over
    assert game.winner == 1

def test_win_vertical():
    """测试垂直方向获胜"""
    game = Gomoku()
    # 黑棋纵向五子
    for row in range(5):
        game.make_move(row, 7)  # 黑棋
        if row < 4:
            game.make_move(row, 8)  # 白棋
    
    assert game.game_over
    assert game.winner == 1

def test_win_diagonal():
    """测试对角线方向获胜"""
    game = Gomoku()
    # 黑棋对角线五子
    for i in range(5):
        game.make_move(i, i)  # 黑棋
        if i < 4:
            game.make_move(i, i+1)  # 白棋
    
    assert game.game_over
    assert game.winner == 1

def test_undo_move():
    """测试撤销移动"""
    game = Gomoku()
    # 进行一些移动
    game.make_move(7, 7)
    game.make_move(7, 8)
    
    # 测试撤销
    assert len(game.history) == 2
    assert game.undo_move()
    assert len(game.history) == 1
    assert game.board[7][8] == 0
    assert game.current_player == 2
    
    assert game.undo_move()
    assert len(game.history) == 0
    assert game.board[7][7] == 0
    assert game.current_player == 1
    
    # 测试空历史记录
    assert not game.undo_move()

def test_board_state():
    """测试棋盘状态"""
    game = Gomoku()
    game.make_move(7, 7)
    state = game.get_board_state()
    assert state[7][7] == 1
    # 确保是副本而不是引用
    state[7][7] = 0
    assert game.board[7][7] == 1 