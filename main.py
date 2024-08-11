import tkinter as tk
from tkinter import messagebox
import random


# Fungsi untuk membuat papan Minesweeper
def create_board(rows, cols, num_mines):
    # Membuat papan kosong
    board = [[' ' for _ in range(cols)] for _ in range(rows)]

    # Menempatkan ranjau secara acak
    placed_mines = 0
    while placed_mines < num_mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if board[row][col] == ' ':
            board[row][col] = 'X'
            placed_mines += 1

    return board


# Fungsi untuk menghitung jumlah ranjau yang bersebelahan dengan sel tertentu
def count_adjacent_mines(board, row, col):
    count = 0
    rows = len(board)
    cols = len(board[0])

    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for dr, dc in neighbors:
        r = row + dr
        c = col + dc

        if 0 <= r < rows and 0 <= c < cols and board[r][c] == 'X':
            count += 1

    return count


# Fungsi untuk mengungkap sel pada papan Minesweeper
def reveal_board(board, minesweeper_board, row, col):
    rows = len(board)
    cols = len(board[0])

    if board[row][col] != ' ':
        return

    mines_count = count_adjacent_mines(minesweeper_board, row, col)

    if mines_count > 0:
        board[row][col] = str(mines_count)
    else:
        board[row][col] = '0'

        neighbors = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in neighbors:
            r = row + dr
            c = col + dc

            if 0 <= r < rows and 0 <= c < cols:
                reveal_board(board, minesweeper_board, r, c)


# Fungsi untuk mengupdate tampilan papan Minesweeper pada GUI
def update_board():
    for r in range(rows):
        for c in range(cols):
            button = buttons[r][c]
            value = board[r][c]

            if value == ' ':
                button.config(text='', relief=tk.RAISED)
            elif value == 'X':
                button.config(text='X', relief=tk.SUNKEN, bg='red', state=tk.DISABLED)
            else:
                button.config(text=value, relief=tk.SUNKEN, bg='light gray', state=tk.DISABLED)


# Fungsi untuk mengecek apakah permainan telah selesai
def check_game_over():
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == ' ':
                return False
            elif board[r][c] == 'X':
                if buttons[r][c]['relief'] != tk.SUNKEN:
                    return False
    return True


# Fungsi yang dipanggil ketika tombol di papan Minesweeper diklik
def button_click(row, col):
    if minesweeper_board[row][col] == 'X':
        messagebox.showinfo('Game Over', 'BOOM! Anda kalah!')
        root.destroy()
    else:
        reveal_board(board, minesweeper_board, row, col)
        update_board()
        if check_game_over():
            messagebox.showinfo('Game Over', 'Selamat! Anda menang!')
            root.destroy()


# Inisialisasi papan Minesweeper
rows = 10
cols = 10
num_mines = 10
board = [[' ' for _ in range(cols)] for _ in range(rows)]
minesweeper_board = create_board(rows, cols, num_mines)

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title('Minesweeper')

buttons = []
for r in range(rows):
    row_buttons = []
    for c in range(cols):
        button = tk.Button(root, width=2, command=lambda r=r, c=c: button_click(r, c))
        button.grid(row=r, column=c)
        row_buttons.append(button)
    buttons.append(row_buttons)

update_board()

root.mainloop()
