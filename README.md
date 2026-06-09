# lecture26_python

## Overview
The repository contains multiple distinct modules, including a Console Banking System, graphical games (Hangman GUI), AI simulations (Chess, Tic-Tac-Toe), and deep learning implementations using PyTorch Transformers.

## Installation Instructions

### Method 1: Conda/Pip Environment Setup (General Dependencies)
For core libraries used across various components (e.g., PySide6, Pygame, Torch):

```bash
pip install torch torchvision numpy pygame PySide6
```

### Method 2: Using Nix Shell (Jupyter Kernel Environment)
To set up a specific development environment with `ipykernel`:

1.  Install dependencies using Nix:
    (Requires running the provided shell definition)
    `nix-shell -p python3 nixpkgs/python3-with-packages`
2.  Run the generated kernel registration command:
    ```bash
    python -m ipykernel install --user --name=nix-env --display-name="Python (Nix)"
    ```

## Modules and Functionality

### 🏦 Banking System (`./ConsoleBank/`)
The banking system manages account data, member information, deposits, and withdrawals using a layered architecture: DAO, Service, and Console.

*   **Data Model:** `Account` class (`./_bank/console_bank.py`): Defines an account with attributes (account number, owner, balance) and methods for deposit and withdrawal.
*   **DAO Layer:** `AccountService` utilizes `AccountDAO` (`./Account/account_dao.py`): Implements CRUD operations on account data stored in an internal dictionary structure (`self.__accountDB`).
*   **Service Logic:** `AccountService` (`./Account/account_service.py`): Encapsulates business logic, handling account creation and transactions (deposit, withdrawal). It requires calls to `AccountDAO`.
*   **Member Management:** The system uses separate modules for membership tracking (`Member/member.py`), data access (`MemberDAO`), and service logic (`MemberService`).

### 🎮 Games Modules

#### Hangman Game
This module provides two implementations of the Hangman game: console text mode and graphical GUI mode.

*   **Terminal Implementation:** `./_etc/hangman.py` utilizes `words.txt` (word list) to select a word randomly. The game tracks attempts and display progress using string manipulation.
*   **GUI Implementation:** `./_Hangman/hangman_gui.py` uses `PySide6` for graphical interaction, defining custom stylesheets for labels, buttons, and the main window structure.

#### Tic-Tac-Toe Game
Two implementations are provided: a console text version and an AI-driven Minimax GUI/console version.

*   **Console Version (`./_etc/tictactoe.py`):** Implements turn-based gameplay with functions to print the board, check for winning conditions (rows, columns, diagonals), and manage player turns ('X' and 'O').
*   **Minimax AI (`./_etc/tictactoe_minmax.py`):** Contains a `minimax` function that calculates optimal moves. The `get_best_move` function utilizes minimax to select the move maximizing the score against the opponent.

#### Chess Game
A GUI application built with Pygame simulating chess gameplay against an AI bot.

*   **Core Components:** Uses `pygame` for display, `python-chess` library for game state management.
*   **AI Bot Logic:** Includes an `evaluate_board` function assigning point values to pieces and a recursive `minimax` function enhanced with Alpha-Beta pruning to determine the optimal move.

### 💡 Utility & ML Modules

#### Command Line Calculator
Simple utility module defining basic arithmetic functions: `add(a, b)`, `sub(a, b)`, `mul(a, b)`, and `div(a, b)`.

#### Stack Operations Simulation
A console program (`./_etc/stack_operation_260330.py`) that simulates stack behavior using an internal list structure (`stack`), implementing methods for:
*   `isFull()`: Checks if the defined capacity is reached.
*   `push(data)`: Adds an element to the top of the stack, respecting capacity limits.
*   `isEmpty()`: Checks if the stack contains elements.
*   `pop()`: Removes and returns the top element.
*   `peak()`: Returns the top element without removing it.

#### PyTorch Transformer Model
This module defines components for a sequence-to-sequence transformer architecture using `torch`.

*   **Classes Defined:**
    *   `PositionalEncoding`: Calculates position embeddings, adding them to input tensors (`x`).
    *   `TransformerGenerator`: The main model class, incorporating embedding layers, positional encoding, and the multi-layer encoder stack.
*   **Methods/Functions:**
    *   `generate_square_subsequent_mask(sz, device)`: Generates a mask used to prevent attention across future tokens during sequence generation.
    *   `load_data(file_path)` (Partial): Function intended for loading data from a specified file path (`data.txt`).

### 🛠️ Environment Scripts

#### Shell Nix Configuration
Defines an isolated Python development environment using `nixpkgs`. The shell script provides pre-installed packages:
*   `ipykernel`
*   `pip`
*   `notebook`