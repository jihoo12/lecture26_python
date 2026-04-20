def print_board(board):
    """보드 상태를 출력합니다."""
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_winner(board):
    """승리 조건을 체크합니다."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # 가로
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # 세로
        [0, 4, 8], [2, 4, 6]             # 대각선
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != " ":
            return board[condition[0]]
    return None

def main():
    # 빈 보드 생성 (1~9 숫자로 위치 가이드 제공 가능)
    board = [" "] * 9
    current_player = "X"
    
    print("--- 틱택토 게임을 시작합니다! ---")
    print("위치 선택은 1부터 9까지의 숫자를 입력하세요.")

    for turn in range(9):
        print_board(board)
        
        try:
            move = int(input(f"플레이어 {current_player}, 위치 선택 (1-9): ")) - 1
            if board[move] != " ":
                print("이미 선택된 자리입니다. 다시 선택하세요.")
                continue
        except (ValueError, IndexError):
            print("잘못된 입력입니다. 1에서 9 사이의 숫자를 입력하세요.")
            continue

        board[move] = current_player
        
        # 승자 확인
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"축하합니다! 플레이어 {winner}가 승리했습니다!")
            return

        # 플레이어 교체
        current_player = "O" if current_player == "X" else "X"

    print_board(board)
    print("무승부입니다!")

if __name__ == "__main__":
    main()