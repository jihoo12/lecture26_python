import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QMessageBox, QGraphicsScene, QGraphicsView)
from PySide6.QtGui import QFont, QPen, QColor, QBrush, QPainter
from PySide6.QtCore import Qt

class HangmanGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Premium Hangman Game")
        self.resize(550, 700)
        
        # 기본 스타일시트 적용 (세련된 다크/그레이 톤 테마)
        self.setStyleSheet("""
            QMainWindow { background-color: #f4f6f9; }
            QLabel#TitleLabel { color: #2c3e50; font-size: 26px; font-weight: bold; }
            QLabel#WordLabel { color: #34495e; font-size: 32px; font-family: 'Courier New'; font-weight: bold; }
            QLabel#StatusLabel { color: #e74c3c; font-size: 14px; font-weight: bold; }
            QPushButton { 
                background-color: #ffffff; color: #2c3e50; 
                border: 1px solid #bdc3c7; border-radius: 6px; 
                font-size: 14px; font-weight: bold; min-width: 40px; min-height: 40px;
            }
            QPushButton:hover { background-color: #ecf0f1; }
            QPushButton:disabled { color: white; }
            QPushButton#ResetButton {
                background-color: #3498db; color: white; border: none;
                font-size: 16px; min-height: 45px; padding: 0 20px;
            }
            QPushButton#ResetButton:hover { background-color: #2980b9; }
        """)

        # 1. 게임 데이터 초기화
        self.words = self.load_words("_Hangman/words.txt")
        self.guessed_letters = []
        self.attempts = 6
        self.letter_buttons = {}

        # 2. UI 레이아웃 설정
        self.setup_ui()
        self.start_new_game()

    def load_words(self, filename):
        try:
            with open(filename, "r") as f:
                return [w.strip() for w in f.readlines() if w.strip()]
        except FileNotFoundError:
            print("words.txt 파일을 찾을 수 없어 기본 단어 목록을 사용합니다.")
            return ["pyside", "interface", "button", "canvas", "window", "developer", "python"]

    def setup_ui(self):
        # 메인 위젯 및 메인 세로 레이아웃
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(15)

        # 상단 타이틀
        title = QLabel("HANGMAN GAME")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # 그래픽 뷰 (Tkinter의 Canvas 역할)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 200, 200)
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(202, 202)
        self.view.setStyleSheet("background-color: white; border: 1px solid #bdc3c7; border-radius: 8px;")
        # 부드러운 선 표현을 위한 안티앨리어싱 설정
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        main_layout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignCenter)

        # 단어 표시 레이블
        self.word_display = QLabel("")
        self.word_display.setObjectName("WordLabel")
        self.word_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.word_display)

        # 남은 기회 레이블
        self.status_label = QLabel("")
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # 알파벳 키보드 프레임 (가로줄 여러 개를 묶을 세로 레이아웃)
        keyboard_layout = QVBoxLayout()
        keyboard_layout.setSpacing(6)
        
        rows = ["ABCDEFGHI", "JKLMNOPQR", "STUVWXYZ"]
        for row in rows:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(5)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for char in row:
                btn = QPushButton(char)
                # 커스텀 람다식으로 클릭한 글자 전달
                btn.clicked.connect(lambda checked=False, c=char.lower(): self.make_guess(c))
                row_layout.addWidget(btn)
                self.letter_buttons[char.lower()] = btn
            keyboard_layout.addLayout(row_layout)
        
        main_layout.addLayout(keyboard_layout)

        # 재시작 버튼
        self.reset_btn = QPushButton("Start New Game")
        self.reset_btn.setObjectName("ResetButton")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.start_new_game)
        main_layout.addWidget(self.reset_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def start_new_game(self):
        self.secret_word = random.choice(self.words).lower()
        self.guessed_letters = []
        self.attempts = 6

        # 캔버스 초기화 및 교수대 그리기
        self.scene.clear()
        self.draw_gallows()

        # 모든 버튼 상태 초기화
        for letter, btn in self.letter_buttons.items():
            btn.setEnabled(True)
            btn.setStyleSheet("") # 스타일시트 초기화로 기본 흰색 복구

        self.update_ui()

    def get_display_word(self):
        return " ".join([l if l in self.guessed_letters else "_" for l in self.secret_word])

    def draw_gallows(self):
        # 선을 그릴 펜 설정 (두께 4, 색상 #34495e)
        pole_pen = QPen(QColor("#34495e"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        rope_pen = QPen(QColor("#e67e22"), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)

        self.scene.addLine(30, 180, 170, 180, pole_pen) # 받침대
        self.scene.addLine(60, 180, 60, 20, pole_pen)   # 기둥
        self.scene.addLine(60, 20, 130, 20, pole_pen)   # 대들보
        self.scene.addLine(130, 20, 130, 45, rope_pen)  # 밧줄

    def draw_man(self):
        man_pen = QPen(QColor("#2c3e50"), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        
        # 기회 상실에 따른 드로잉 순서 정의 (람다 함수 리스트)
        parts = [
            lambda: self.scene.addEllipse(115, 45, 30, 30, man_pen),               # 머리 (x, y, w, h)
            lambda: self.scene.addLine(130, 75, 130, 130, man_pen),                # 몸통
            lambda: self.scene.addLine(130, 85, 105, 105, man_pen),                # 왼팔
            lambda: self.scene.addLine(130, 85, 155, 105, man_pen),                # 오른팔
            lambda: self.scene.addLine(130, 130, 105, 165, man_pen),               # 왼다리
            lambda: self.scene.addLine(130, 130, 155, 165, man_pen)                # 오른다리
        ]
        
        index = 5 - self.attempts
        if index < len(parts):
            parts[index]()

    def make_guess(self, letter):
        if letter in self.guessed_letters:
            return

        self.guessed_letters.append(letter)
        btn = self.letter_buttons[letter]
        btn.setEnabled(False)

        if letter in self.secret_word:
            # 정답일 때: 초록색 버튼
            btn.setStyleSheet("background-color: #2ecc71; color: white; border: none;")
        else:
            # 오답일 때: 회색 버튼 및 기회 참감
            btn.setStyleSheet("background-color: #95a5a6; color: white; border: none;")
            self.attempts -= 1
            self.draw_man()

        self.update_ui()
        # QTimer.singleShot 대신 이벤트 루프가 UI를 그리고 즉시 판정하도록 넘깁니다.
        QApplication.processEvents() 
        self.check_game_over()

    def update_ui(self):
        self.word_display.setText(self.get_display_word())
        self.status_label.setText(f"Attempts Left: {self.attempts} / 6")

    def check_game_over(self):
        if "_" not in self.get_display_word():
            QMessageBox.information(self, "Victory!", f"Congratulations!\nYou guessed the word:\n\n{self.secret_word.upper()}")
            self.start_new_game()
        elif self.attempts <= 0:
            QMessageBox.information(self, "Game Over", f"Oops! Out of attempts.\nThe correct word was:\n\n{self.secret_word.upper()}")
            self.start_new_game()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = HangmanGUI()
    game.show()
    sys.exit(app.exec())