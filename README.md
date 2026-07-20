# 🎮 Connect 4 AI

A classic Connect 4 game built with **Streamlit**, featuring an AI opponent powered by the **Minimax algorithm with Alpha-Beta pruning**. Play against a smart AI that thinks ahead, blocks your winning moves, and looks for its own opportunities to win.

---

## ✨ Features

- 🕹️ Interactive 7×6 game board rendered in the browser
- 🤖 AI opponent using Minimax + Alpha-Beta pruning (configurable search depth)
- 🎯 Heuristic scoring that rewards center control, connected pieces, and blocking threats
- ⚡ Instant-win detection — the AI takes a winning move immediately if one is available
- 🔄 "Play Again" reset without restarting the app
- 🎨 Custom-styled board and pieces (red vs. yellow discs)

---

## 📁 Project Structure

```
connect4-ai/
├── app.py            # Streamlit UI — game loop, rendering, session state
├── game_board.py      # Connect4Board class — board state, moves, win detection
├── ai_strategy.py      # Connect4AI class — Minimax with Alpha-Beta pruning
└── README.md
```

| File | Responsibility |
|---|---|
| `game_board.py` | Owns the board state (`numpy` grid), validates moves, drops pieces, and checks for horizontal/vertical/diagonal wins or a full board. |
| `ai_strategy.py` | Implements the AI's decision-making: scores board positions, runs Minimax with Alpha-Beta pruning, and returns the AI's chosen column. |
| `app.py` | Streamlit front end — draws the board, wires up column buttons, manages turns, and shows win/draw/reset states. |

---

## 🧠 How the AI Works

1. **Immediate win check** — before searching, the AI checks if any move wins the game outright and plays it right away.
2. **Minimax search** — otherwise, it simulates future moves up to a fixed `depth`, alternating between maximizing the AI's outcome and minimizing the human's.
3. **Alpha-Beta pruning** — cuts off branches that can't affect the final decision, making deeper searches fast.
4. **Position scoring** (when the search doesn't reach a finished game) weighs:
   - Center column control (+3 per piece)
   - Windows of 4 cells with 2, 3, or 4 of the AI's pieces
   - Blocking the opponent when they have 3-in-a-row with an open spot

You can tune the difficulty by changing the `depth` passed to `Connect4AI` in `app.py` (currently `depth=4`). Higher = smarter but slower.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+ installed
- `pip` available on your PATH

### 2. Clone or download the project
Place `app.py`, `game_board.py`, and `ai_strategy.py` in the same folder.

### 3. Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install streamlit numpy
```

### 5. Run the app
From inside the project folder:
```bash
streamlit run app.py
```

Streamlit will start a local server and automatically open the game in your browser (usually at `http://localhost:8501`).

---

## 🕹️ How to Play

1. Click a numbered column button (1–7) to drop your piece.
2. You play as **red**; the AI plays as **yellow**.
3. Connect **4 pieces in a row** — horizontally, vertically, or diagonally — to win.
4. If the board fills up with no winner, it's a draw.
5. Click **"Play Again"** to reset and start a new round.

---

## 🛠️ Requirements

```
streamlit
numpy
```

You can save these into a `requirements.txt` file:
```bash
pip freeze > requirements.txt
```

---

## 📌 Notes & Possible Improvements

- The AI's `depth` is currently hardcoded to `4` in `app.py`; exposing this as a UI slider (e.g., "Easy / Medium / Hard") would let players adjust difficulty.
- Board copying in `minimax()` recreates a full `Connect4Board` object per branch — for very high depths this could be optimized (e.g., undo-move instead of copy) if performance becomes an issue.
- Adding a move-history/undo feature and a scoreboard across multiple rounds would extend replayability.
