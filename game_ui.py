from gomoku import Gomoku

def print_instructions():
    """打印游戏说明"""
    print("\n欢迎来到五子棋游戏！")
    print("游戏说明：")
    print("1. 输入行号(0-14)和列号(0-14)来放置棋子")
    print("2. ●表示黑子，○表示白子")
    print("3. 输入'u'可以撤销上一步")
    print("4. 输入'q'可以退出游戏")
    print("5. 先把五个棋子连成一线的玩家获胜\n")

def play_game():
    """运行游戏主循环"""
    game = Gomoku()
    print_instructions()
    
    while not game.game_over:
        game.display_board()
        current = "黑棋" if game.current_player == 1 else "白棋"
        print(f"\n当前玩家：{current}")
        
        move = input("请输入移动 (行 列)，'u'撤销，'q'退出: ").strip().lower()
        
        if move == 'q':
            print("\n游戏结束！")
            return
        elif move == 'u':
            if game.undo_move():
                print("\n已撤销上一步移动")
            else:
                print("\n无法撤销：没有更多移动记录")
            continue
            
        try:
            row, col = map(int, move.split())
            if not game.make_move(row, col):
                print("\n无效的移动，请重试！")
                continue
                
        except (ValueError, IndexError):
            print("\n请输入有效的坐标！格式：行号 列号（例如：7 7）")
            continue
            
    game.display_board()
    if game.winner:
        winner = "黑棋" if game.winner == 1 else "白棋"
        print(f"\n游戏结束！{winner}获胜！")

if __name__ == "__main__":
    play_game() 