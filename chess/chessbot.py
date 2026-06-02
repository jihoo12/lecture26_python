import pygame
import chess
import sys

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Color Palette (RGB)
LIGHT_SQ = (235, 236, 240)    # Off-white
DARK_SQ = (119, 154, 88)      # Matte Green
HIGHLIGHT_COLOR = (186, 202, 43) # Lime yellow for selected square
TEXT_COLOR = (0, 0, 0)        # Black for pieces

# Setup Window and Font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess Game vs AI")
font = pygame.font.SysFont("segoeuihistoric", 50) 

# Dictionary mapping python-chess symbols to Unicode characters
UNICODE_PIECES = {
    'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
    'r': '環境', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙'
}

# --- AI BOT LOGIC SYSTEM ---

def evaluate_board(board):
    """Simple board evaluation function."""
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999
    if board.is_game_over():
        return 0 # Draw/Stalemate

    # Point values for white pieces (positive) and black pieces (negative)
    piece_values = {
        chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, 
        chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
    }
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += val
            else:
                score -= val
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax search algorithm enhanced with Alpha-Beta pruning."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        # Simple sorting technique: check capture moves first to optimize alpha-beta pruning speed
        moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)
        for move in moves:
            board.push(move)
            evaluation, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)
        for move in moves:
            board.push(move)
            evaluation, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, best_move

# --- GRAPHICS RENDERING SYSTEM ---

def draw_board(screen, selected_square):
    """Draws the alternating checkered grid and highlights the selected square."""
    for r in range(ROWS):
        for c in range(COLS):
            color = LIGHT_SQ if (r + c) % 2 == 0 else DARK_SQ
            square_index = chess.square(c, 7 - r)
            if selected_square == square_index:
                color = HIGHLIGHT_COLOR
                
            pygame.draw.rect(screen, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    """Renders the Unicode characters onto their respective squares."""
    # Fixed lookup table strings mapping to proper display glyph symbols
    PIECE_GLYPHS = { 'R': 'rw', 'N': 'nw', 'B': 'bw', 'Q': 'qw', 'K': 'kw', 'P': 'pw', 
                    'r': 'rb', 'n': 'nb', 'b': 'bb', 'q': 'qb', 'k': 'kb', 'p': 'pb' }
    for r in range(ROWS):
        for c in range(COLS):
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            if piece:
                char = PIECE_GLYPHS.get(piece.symbol(), '')
                text_surface = font.render(char, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(text_surface, text_rect)

# --- MAIN LOOP ---

def main():
    board = chess.Board()
    selected_square = None
    clock = pygame.time.Clock()

    print("Game Started! You are playing White. Make your first move.")

    while True:
        # --- BOT MOVE CHECKER ---
        if not board.is_game_over() and board.turn == chess.BLACK:
            # Force graphics refresh before starting a heavy AI calculation
            draw_board(screen, selected_square)
            draw_pieces(screen, board)
            pygame.display.flip()
            
            print("AI Engine is thinking...")
            # Run search tree depth 3 (Balances processing speed and bot intelligence)
            _, bot_move = minimax(board, depth=3, alpha=-float('inf'), beta=float('inf'), maximizing_player=False)
            
            if bot_move:
                board.push(bot_move)
                print(f"AI played: {bot_move}")
                if board.is_game_over():
                    print("Game Over!", board.result())

        # --- USER INPUT CHECKER ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE and not board.is_game_over():
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                clicked_square = chess.square(col, 7 - row)

                if selected_square is None:
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == chess.WHITE:
                        selected_square = clicked_square
                else:
                    move = chess.Move(selected_square, clicked_square)
                    
                    # Manage pawn promotions automatically to a Queen
                    if board.piece_at(selected_square) and board.piece_at(selected_square).piece_type == chess.PAWN:
                        if chess.square_rank(clicked_square) == 7:
                            move.promotion = chess.QUEEN

                    if move in board.legal_moves:
                        board.push(move)
                        print(f"You played: {move}")
                        if board.is_game_over():
                            print("Game Over!", board.result())
                    else:
                        print("Illegal move! Try again.")
                        
                    selected_square = None

        # Redraw screen elements
        draw_board(screen, selected_square)
        draw_pieces(screen, board)
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()