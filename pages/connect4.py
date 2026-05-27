import streamlit as st

import copy

rows_number = 6
cols_number = 7

empty_cell = "🟢"
player_cell = "🔵"
comp_cell = "🔴"

def create_virtual_board(board,player,col):
    temp_board = copy.deepcopy(board)

    for r in range(rows_number - 1, -1, -1):
        if temp_board[r][col] == empty_cell:
            temp_board[r][col] = player
            break

    return temp_board

def newBoard():
    board = []
    for row in range(rows_number):
        row = []
        for cell in range(cols_number):
            row.append(empty_cell)
        board.append(row)

    st.session_state.board = board

if not "board" in st.session_state:
    newBoard()

board = st.session_state.board

if "turn" not in st.session_state:
    st.session_state.turn = player_cell

turn = st.session_state.turn

def calc_score(range4,good):
    bad = player_cell if good == comp_cell else comp_cell

    score = 0
    if range4.count(good) == 4:
        score += 100
    elif range4.count(good) == 3 and range4.count(empty_cell) == 1:
        score += 50
    elif range4.count(good) == 2 and range4.count(empty_cell) == 2:
        score += 10

    if range4.count(bad) == 3 and range4.count(empty_cell) == 1:
        score -= 75
    elif range4.count(bad) == 2 and range4.count(empty_cell) == 2:
        score -= 30


    #print(good,range4,score)
    return score

def calc_board_score(board,good):
    score = 0

    for r in range(rows_number):
        row = board[r]
        for c in range(cols_number - 3):
            range4 = row[r:r+4]
            score += calc_score(range4,good)

    for c in range(cols_number):
        col = [board[r][c] for r in range(rows_number)]
        for r in range(rows_number - 3):
            range4 = col[r:r+4]
            score += calc_score(range4,good)

    for r in range(rows_number - 3):
        for c in range(cols_number - 3):
            range4 = [board[r+i][c+i] for i in range(4)]
            score += calc_score(range4,good)

            range4 = [board[r-3+i][c+i] for i in range(4)]
            score += calc_score(range4,good)

    middle_number = cols_number // 2
    middle_col = [board[r][middle_number] for r in range(rows_number)]
    score += middle_col.count(good) * 5

    right_col = [board[r][middle_number + 1] for r in range(rows_number)]
    score += right_col.count(good) * 2

    left_col = [board[r][middle_number - 1] for r in range(rows_number)]
    score += left_col.count(good) * 2

    return score

    #print(good,":",score)
#calc_board_score(board,turn)

def switchturn ():
    global turn
    if turn == player_cell:
        turn = comp_cell
    else:
        turn = player_cell
    st.session_state.turn = turn

def check(row,col, player):
    print(f"checking row {row} col {col}")

    for cell in range(0, cols_number - 3):
        if board[row][cell] == empty_cell:
            continue
        if board[row][cell] != player:
            continue

        number = 0
        for i in range(cell,cell + 4):
            if board[row][i] == board[row][cell]:
                number +=1
            else:
                break
        if number == 4:
            print(player)
            st.session_state.winner = player
            return


    for cell in range(0, rows_number - 3):
        if board[cell][col] == empty_cell:
            continue
        if board[cell][col] != player:
            continue

        number = 0
        for i in range(cell, cell + 4):
            if board[i][col] == board[cell][col]:
                number += 1
            else:
                break
        if number == 4:
            print(player)
            st.session_state.winner = player
            return
#########################################################################
    offset = min(col,row)
    start_row = row - offset
    start_col = col - offset

    number = 0
    for i in range(cols_number):
        check_row = start_row + i
        check_col = start_col + i
        if check_col == cols_number or check_row == rows_number:
            print("אין רצף")
            break

        print(f"player: {player} row: {check_row} col: {check_col}")
        if board[check_row][check_col] == player:
            number += 1
        else:
            number = 0
        if number == 4:
            print(player)
            st.session_state.winner = player
            return

    dist_left = col
    dist_bottom = rows_number - 1 -row
    offset = min(dist_left,dist_bottom)

    start_row = row + offset
    start_col = col - offset

    number = 0
    for i in range(cols_number):
        check_row = start_row - i
        check_col = start_col + i

        if check_row < 0 or check_col >= cols_number:
            break

        if board[check_row][check_col] == player:
            number += 1
        else:
            number = 0

        if number == 4:
            print(player)
            st.session_state.winner = player
            return


def click(col):
    if board[0][col] != empty_cell:
        st.rerun()
    for row in range (rows_number - 1, -1, -1):
        if board[row][col] == empty_cell:
            board[row][col] = turn
            check(row,col,turn)
            break

    #board[rows_number - 1][col] = player_cell
    switchturn()
    st.session_state.board = board
    st.rerun()

def computer_play():
    import random, time
    #time.sleep (0.23)
    #col = random.randint(0,cols_number - 1)
    best_score = -2248726572463763536325652987
    best_col = -1
    for c in range(cols_number):
        if board[0][c] != empty_cell:
            continue

        temp_board = create_virtual_board(board,comp_cell,c)
        score = calc_board_score(temp_board,comp_cell)

        if best_score < score:
            best_score = score
            best_col = c
        print(f"{c}: {score}")
    click(best_col)

    #click(col)

if "winner" not in st.session_state:
    st.session_state.winner = ""

winner = st.session_state.winner

has_empty = False
for col in range(cols_number):
    if board[0][col] == empty_cell:
        has_empty = True
        break

if winner == comp_cell:
    st.info("המחשב ניצח")
elif winner == player_cell:
    st.info("ניצחת")
elif not has_empty:
    st.info("תיקו")
else:
    if turn == player_cell:
        st.info("התור שלך")
    else:
        st.status("המחשב חושב...")

for row in range (rows_number): #עבור כל שורה
    all_column = st.columns(cols_number) #לכל שורה - צור תאים
    #שמים בתאים
    for col in range(cols_number): #תעבור על כל תא לפי מספר התאים
        with all_column[col]: #כניסה לעמודה
            cell = board[row][col] #שולפים מהזיכרון מה אמור להיות בתא
            if st.button(cell, key=f"row_{row}_col_{col}",
                         use_container_width=True,
                         disabled = turn==comp_cell or winner !=""):
                click(col)

if turn == comp_cell and winner == "" and has_empty:
    computer_play()








































































































































































