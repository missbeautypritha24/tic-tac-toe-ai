import streamlit as st
import math

st.set_page_config(page_title="Tic Tac Toe with AI", page_icon="🎮", layout="centered")
st.title("🎮 Tic Tac Toe - Play vs Unbeatable AI")

if 'board' not in st.session_state:
    st.session_state.board = [" "] * 9
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None

def check_winner(board, player):
    combos = [[0,1,2],[3,4,5],[6,7,8],
              [0,3,6],[1,4,7],[2,5,8],
              [0,4,8],[2,4,6]]
    return any(all(board[i] == player for i in combo) for combo in combos)

def is_draw(board):
    return all(cell != " " for cell in board)

def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == " "]

def minimax(board, is_max):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_draw(board):
        return 0

    if is_max:
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move] = "O"
            score = minimax(board, False)
            board[move] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(board):
            board[move] = "X"
            score = minimax(board, True)
            board[move] = " "
            best_score = min(score, best_score)
        return best_score

def get_best_move(board):
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        board[move] = "O"
        score = minimax(board, False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def player_move(move):
    if st.session_state.board[move] == " " and not st.session_state.game_over:
        st.session_state.board[move] = "X"

        if check_winner(st.session_state.board, "X"):
            st.session_state.game_over = True
            st.session_state.winner = "You"
        elif is_draw(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = "Draw"
        else:
            ai_move()

def ai_move():
    move = get_best_move(st.session_state.board)
    if move is not None:
        st.session_state.board[move] = "O"

    if check_winner(st.session_state.board, "O"):
        st.session_state.game_over = True
        st.session_state.winner = "AI"
    elif is_draw(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "Draw"

for i in range(0, 9, 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j
        if st.session_state.board[idx] == " ":
            if cols[j].button(" ", key=idx):
                player_move(idx)
        else:
            cols[j].markdown(f"### `{st.session_state.board[idx]}`")

if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.success("🤝 It's a draw!")
    else:
        st.success(f"🎉 {st.session_state.winner} wins!")

if st.button("🔁 Restart Game"):
    st.session_state.board = [" "] * 9
    st.session_state.game_over = False
    st.session_state.winner = None
