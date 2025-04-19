# app.py
import streamlit as st
import numpy as np
import time
from game_board import Connect4Board
from ai_strategy import Connect4AI

# Page configuration
st.set_page_config(
    page_title="Connect 4 AI",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# App title and description
st.title("Connect 4 Game")
st.markdown("""
This is a Connect 4 game implementation using Minimax Algorithm with Alpha-Beta Pruning.
Play against the AI by clicking on the column where you want to drop your piece.
""")

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = Connect4Board()
    st.session_state.ai = Connect4AI(depth=4)  # Adjust depth for difficulty
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.difficulty = 4
    st.session_state.processing = False

# Difficulty settings in sidebar
st.sidebar.title("Game Settings")
difficulty = st.sidebar.select_slider(
    "AI Difficulty",
    options=[1, 2, 3, 4, 5],
    value=st.session_state.difficulty,
    help="Higher values make the AI smarter but slower"
)

if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.ai = Connect4AI(depth=difficulty)
    st.experimental_rerun()

# Custom CSS for styling
st.markdown("""
<style>
    .board-container {
        display: flex;
        justify-content: center;
        margin: 10px 0;
    }
    .board {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 30px;
        background-color: #2C3E50;
        padding: 10px;
        border-radius: 7px;
    }
    .cell {
        width: 75px;
        height: 75px;
        border-radius: 50%;
        background-color: #ECF0F1;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .player1 {
        background-color: #E74C3C;
    }
    .player2 {
        background-color: #F1C40F;
    }
    .col-button {
        background-color: #3498DB;
        color: white;
        border: none;
        border-radius: 4px;
        padding-left: 20px;
        padding-right: 20px;
        width: 100%;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .col-button:hover {
        background-color: #2980B9;
    }
    .col-button:disabled {
        background-color: #95A5A6;
        cursor: not-allowed;
    }
    .stButton>button {
        padding-left: 40px;
        padding-right: 40px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Function to render the board
def render_board():
    board_html = '<div class="board-container"><div class="board">'
    
    # Create cells for each position
    for row in range(st.session_state.board.rows):
        for col in range(st.session_state.board.cols):
            cell_class = "cell"
            cell_value = st.session_state.board.board[row][col]
            
            if cell_value == 1:
                cell_class += " player1"
            elif cell_value == 2:
                cell_class += " player2"
                
            board_html += f'<div class="{cell_class}"></div>'
    
    board_html += '</div></div>'
    st.markdown(board_html, unsafe_allow_html=True)

# Function to handle player move
def make_move(col):
    # Check if game is over or move is invalid
    if st.session_state.game_over or not st.session_state.board.is_valid_move(col) or st.session_state.processing:
        return
    
    # Set processing flag to true to prevent multiple moves
    st.session_state.processing = True

    # Player move
    st.session_state.board.drop_piece(col, 1)
    
    # Check if player won
    if st.session_state.board.check_winner(1):
        st.session_state.game_over = True
        st.session_state.winner = "Player"
        st.session_state.processing = False  # Reset processing flag
        return
    
    # Check for draw
    if st.session_state.board.is_board_full():
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
        st.session_state.processing = False  # Reset processing flag
        return
    
    # AI move with a small delay for better UX
    with st.spinner("AI is thinking..."):
        # Add a small delay to show the spinner
        time.sleep(0.5)
        
        # Get AI move
        ai_col = st.session_state.ai.get_best_move(st.session_state.board)
        
        # Make AI move
        st.session_state.board.drop_piece(ai_col, 2)
    
    # Check if AI won
    if st.session_state.board.check_winner(2):
        st.session_state.game_over = True
        st.session_state.winner = "AI"
        return
    
    # Check for draw again
    if st.session_state.board.is_board_full():
        st.session_state.game_over = True
        st.session_state.winner = "Draw"

    # Reset processing flag
    st.session_state.processing = False

# Reset game function
def reset_game():
    st.session_state.board.reset_board()
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.processing = False

# Column selection buttons
st.markdown("### Select a column to drop your piece")
cols = st.columns(7)
for i, col in enumerate(cols):
    is_valid = st.session_state.board.is_valid_move(i)
    with col:
        st.button(
            f"{i + 1}", 
            key=f"col_{i}",
            on_click=make_move,
            args=(i,),
            disabled = not is_valid or st.session_state.game_over or st.session_state.processing
        )

# Display the board
render_board()

# Game status display
if st.session_state.game_over:
    if st.session_state.winner == "Player":
        st.success("🎉 Congratulations! You won!")
    elif st.session_state.winner == "AI":
        st.error("🤖 The AI won this time. Try again!")
    else:
        st.info("🤝 It's a draw!")
    
    # Reset button
    if st.button("Play Again", key="reset_button"):
        reset_game()
else:
    # Show current turn status
    st.info("Your turn! Click a column to drop your piece.")

# Game instructions and information
with st.expander("How to Play"):
    st.markdown("""
    ### Rules:
    1. Players take turns dropping colored discs into the grid
    2. The pieces fall straight down and occupy the lowest available space
    3. The objective is to connect 4 of your discs vertically, horizontally, or diagonally
    4. The first player to connect 4 discs wins
    
    ### About the AI:
    This game uses the Minimax algorithm with Alpha-Beta pruning to create an AI opponent. 
    The algorithm works by:
    - Exploring possible future game states
    - Evaluating the best moves for both players
    - Choosing the optimal move based on this evaluation
    - Using Alpha-Beta pruning to optimize the search
    
    Adjust the difficulty level in the sidebar to change how many moves ahead the AI considers.
    """)

# Add information about the project
st.markdown("---")
st.markdown("### Connect 4 with Minimax and Alpha-Beta Pruning")
st.markdown("Implemented using Streamlit, NumPy, and the Minimax algorithm")