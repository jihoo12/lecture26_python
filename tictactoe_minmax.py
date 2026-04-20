import math

# 보드 초기화
board = [' ' for _ in range(9)]

def print_board():
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6: print("-----------")

def check_winner(b, p):
    # 승리 조건 (가로, 세로, 대각선)
    win_states = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    return any(b[s[0]] == b[s[1]] == b[s[2]] == p for s in win_states)

def is_full(b):
    return ' ' not in b

def minimax(b, depth, is_maximizing):
    # 1. 종료 조건 확인 및 점수 반환
    if check_winner(b, 'O'): return 10 - depth  # AI 승리 (빠를수록 높은 점수)
    if check_winner(b, 'X'): return depth - 10  # 사람 승리
    if is_full(b): return 0                     # 비김

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O'
                score = minimax(b, depth + 1, False)
                b[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'X'
                score = minimax(b, depth + 1, True)
                b[i] = ' '
                best_score = min(score, best_score)
        return best_score

def get_best_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

# 게임 루프
while True:
    print_board()
    # 사람의 턴
    human_move = int(input("어디에 두시겠습니까? (0-8): "))
    if board[human_move] != ' ': continue
    board[human_move] = 'X'
    
    if check_winner(board, 'X'):
        print_board(); print("당신이 이겼습니다!"); break
    if is_full(board):
        print_board(); print("비겼습니다!"); break

    # AI의 턴
    print("\nAI가 생각 중입니다...")
    ai_move = get_best_move()
    board[ai_move] = 'O'

    if check_winner(board, 'O'):
        print_board(); print("AI가 이겼습니다!"); break
    if is_full(board):
        print_board(); print("비겼습니다!"); break
