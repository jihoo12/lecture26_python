import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QMessageBox, QGraphicsScene, QGraphicsView)
from PySide6.QtGui import QFont, QPen, QColor, QBrush, QPainter, QKeyEvent, QFontDatabase
from PySide6.QtCore import Qt

class HangmanGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Premium Hangman Game")
        self.setMinimumSize(600, 750)
        
        # [핵심 추가] 애플리케이션 전체에 시스템 이모지 폰트를 최우선 폰트로 강제 주입
        # 윈도우 시스템의 이모지 폰트를 강제로 앱 엔진에 등록합니다.
        QApplication.setFont(QFont("Segoe UI Emoji", 10))
        
        # 스타일시트에서 복잡하게 폰트를 꼬아놓으면 이모지가 깨지므로, 
        # 웹 스타일 대신 깔끔하게 정리하고 자간 및 특수 기호를 텍스트 기반으로 안정화했습니다.
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e24; }
            QLabel#TitleLabel { color: #fff; font-size: 28px; font-weight: 900; }
            
            QLabel#WordLabel { 
                color: #f7fff7; 
                font-size: 36px; 
                font-family: 'Consolas', 'Courier New', 'Segoe UI Emoji'; 
                font-weight: bold; 
            }
            
            QLabel#StatusLabel { 
                color: #ff6b6b; 
                font-size: 16px; 
                font-weight: bold; 
                font-family: 'Segoe UI', 'Malgun Gothic', 'Segoe UI Emoji';
            }
            
            QLabel#ScoreLabel { 
                color: #4ecdc4; 
                font-size: 14px; 
                font-weight: bold; 
                font-family: 'Segoe UI', 'Malgun Gothic', 'Segoe UI Emoji';
            }
            
            QPushButton { 
                background-color: #2f313d; color: #f7fff7; 
                border: none; border-radius: 8px; 
                font-size: 15px; font-weight: bold; min-width: 45px; min-height: 45px;
                font-family: 'Segoe UI', 'Malgun Gothic', 'Segoe UI Emoji';
            }
            QPushButton:hover { background-color: #414455; }
            
            QPushButton#ResetButton {
                background-color: #ff6b6b; color: white; border: none; border-radius: 20px;
                font-size: 16px; font-weight: bold; min-height: 45px; padding: 0 30px;
                font-family: 'Segoe UI', 'Malgun Gothic', 'Segoe UI Emoji';
            }
            QPushButton#ResetButton:hover { background-color: #ff8787; }
        """)

        # 게임 데이터 및 메트릭 초기화
        self.words = self.load_words("_Hangman/words.txt")
        self.guessed_letters = set()
        self.attempts = 6
        self.letter_buttons = {}
        
        # 점수 시스템 추가
        self.score = 0
        self.streak = 0

        self.setup_ui()
        self.start_new_game()

    def load_words(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return [w.strip().lower() for w in f.readlines() if w.strip()]
        except FileNotFoundError:
            print("words.txt 파일을 찾을 수 없어 내장된 개발자 단어 목록을 사용합니다.")
            return ["pyside", "interface", "button", "canvas", "window", "developer", "python", "rust", "lambda"]

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 상단 헤더 (타이틀 & 점수판)
        header_layout = QHBoxLayout()
        title = QLabel("HANGMAN")
        title.setObjectName("TitleLabel")
        
        # 폰트 깨짐이 너무 심할 경우를 대비해 불이모지(🔥) 대신 디자인 텍스트 [STREAK] 로 안 깨지게 마감 처리 가능
        # 여기서는 이모지 폰트 강제 주입을 시도합니다.
        self.score_label = QLabel("Score: 0  |  Streak: 0 🔥")
        self.score_label.setObjectName("ScoreLabel")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.score_label)
        main_layout.addLayout(header_layout)

        # 그래픽 뷰 (행맨 캔버스)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 220, 220)
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(222, 222)
        self.view.setStyleSheet("background-color: #2f313d; border: 2px solid #414455; border-radius: 12px;")
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_layout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignCenter)

        # 단어 표시 레이블
        self.word_display = QLabel("")
        self.word_display.setObjectName("WordLabel")
        self.word_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.word_display)

        # 상태 메시지 레이블
        self.status_label = QLabel("")
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # 가상 키보드 레이아웃
        keyboard_layout = QVBoxLayout()
        keyboard_layout.setSpacing(8)
        
        rows = ["ABCDEFGHI", "JKLMNOPQR", "STUVWXYZ"]
        for row in rows:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(6)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for char in row:
                btn = QPushButton(char)
                letter = char.lower()
                btn.clicked.connect(lambda checked=False, l=letter: self.make_guess(l))
                row_layout.addWidget(btn)
                self.letter_buttons[letter] = btn
            keyboard_layout.addLayout(row_layout)
        
        main_layout.addLayout(keyboard_layout)
        main_layout.addSpacing(10)

        # 제어 버튼 (➔ 기호는 유니코드 기본 특수기호라 절대 깨지지 않습니다)
        self.reset_btn = QPushButton("Next Word ➔")
        self.reset_btn.setObjectName("ResetButton")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.start_new_game)
        main_layout.addWidget(self.reset_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def start_new_game(self):
        if not self.words:
            self.status_label.setText("단어 목록이 비어있습니다.")
            return
            
        self.secret_word = random.choice(self.words).lower()
        self.guessed_letters.clear()
        self.attempts = 6

        self.scene.clear()
        self.draw_gallows()

        # 키보드 버튼 스타일 초기화 및 활성화
        for letter, btn in self.letter_buttons.items():
            btn.setEnabled(True)
            btn.setStyleSheet("")

        self.update_ui()

    def get_display_word(self, reveal_all=False):
        result = []
        for l in self.secret_word:
            if l in self.guessed_letters:
                result.append(l.upper())
            else:
                result.append("_" if not reveal_all else f"<span style='color: #ff6b6b;'>{l.upper()}</span>")
        
        return "   ".join(result)

    def draw_gallows(self):
        pole_pen = QPen(QColor("#ffb86c"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        rope_pen = QPen(QColor("#ff79c6"), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)

        self.scene.addLine(40, 190, 180, 190, pole_pen) 
        self.scene.addLine(70, 190, 70, 30, pole_pen)   
        self.scene.addLine(70, 30, 140, 30, pole_pen)   
        self.scene.addLine(140, 30, 140, 55, rope_pen)  

    def draw_man(self):
        man_pen = QPen(QColor("#f8f8f2"), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        
        parts = [
            lambda: self.scene.addEllipse(125, 55, 30, 30, man_pen),               
            lambda: self.scene.addLine(140, 85, 140, 140, man_pen),                
            lambda: self.scene.addLine(140, 95, 115, 115, man_pen),                
            lambda: self.scene.addLine(140, 95, 165, 115, man_pen),                
            lambda: self.scene.addLine(140, 140, 115, 175, man_pen),               
            lambda: self.scene.addLine(140, 140, 165, 175, man_pen)                
        ]
        
        index = 5 - self.attempts
        if index < len(parts):
            parts[index]()

    def make_guess(self, letter):
        if letter in self.guessed_letters or self.attempts <= 0:
            return

        self.guessed_letters.add(letter)
        btn = self.letter_buttons.get(letter)
        
        if btn:
            btn.setEnabled(False)

        if letter in self.secret_word:
            if btn:
                btn.setStyleSheet("background-color: #2ecc71; color: white; border: none;")
            if all(l in self.guessed_letters for l in self.secret_word):
                self.update_ui()
                QApplication.processEvents()
                self.handle_game_over(victory=True)
                return
        else:
            if btn:
                btn.setStyleSheet("background-color: #ff6b6b; color: white; border: none;")
            self.attempts -= 1
            self.draw_man()
            
            if self.attempts <= 0:
                self.update_ui()
                QApplication.processEvents()
                self.handle_game_over(victory=False)
                return

        self.update_ui()

    def update_ui(self):
        self.word_display.setText(self.get_display_word(reveal_all=False))
        # 만약 폭발 이모지(💥)가 깨진다면 이 줄을 다음과 같이 수정하세요: f"[!] Attempts Left: {self.attempts} / 6"
        self.status_label.setText(f"💥 Attempts Left: {self.attempts} / 6")
        # 만약 불이모지(🔥)가 깨진다면 이 줄을 다음과 같이 수정하세요: f"Score: {self.score}  |  Streak: {self.streak} [MAX]"
        self.score_label.setText(f"Score: {self.score}  |  Streak: {self.streak} 🔥")

    def handle_game_over(self, victory):
        if victory:
            self.streak += 1
            self.score += 10 + (self.streak * 2)
            # 알림창 이모지 깨짐 방지용 텍스트 문구 수정
            QMessageBox.information(self, "Victory!", f"Great Job!\nYou guessed the word:\n\n{self.secret_word.upper()}\n\n+Score gained!")
        else:
            self.streak = 0 
            self.word_display.setText(self.get_display_word(reveal_all=True))
            # 알림창 이모지 깨짐 방지용 텍스트 문구 수정
            QMessageBox.critical(self, "Game Over", f"Out of attempts!\nThe correct word was:\n\n{self.secret_word.upper()}")
        
        self.start_new_game()

    def keyPressEvent(self, event: QKeyEvent):
        key_text = event.text().lower()
        if key_text.isalpha() and len(key_text) == 1 and key_text in self.letter_buttons:
            if self.letter_buttons[key_text].isEnabled():
                self.make_guess(key_text)
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = HangmanGUI()
    game.show()
    sys.exit(app.exec())