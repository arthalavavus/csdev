import tkinter as tk
from tkinter import messagebox

class Puissance4:   # ne renvoie rien si le tableau est plein on ne peut pas relancer de partie
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Puissance 4")

        self.rows = 6
        self.cols = 7
        self.current_player = "red"

        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_ui()

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="blue")
        self.canvas.pack()

        for row in range(self.rows):
            for col in range(self.cols):
                x0 = col * 100
                y0 = row * 100
                x1 = x0 + 100
                y1 = y0 + 100
                self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="white", tags=f"cell-{row}-{col}")

        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        col = event.x // 100

        if col < 0 or col >= self.cols:
            return

        row = self.get_available_row(col)

        if row is not None:
            self.board[row][col] = self.current_player
            self.draw_piece(row, col)

            if self.check_winner(row, col):
                messagebox.showinfo("Félicitations", f"Le joueur {self.current_player} a gagné !")
                self.reset_game()
                return

            self.switch_player()

    def get_available_row(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] is None:
                return row
        return None

    def draw_piece(self, row, col):
        x0 = col * 100
        y0 = row * 100
        x1 = x0 + 100
        y1 = y0 + 100

        self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill=self.current_player, tags=f"piece-{row}-{col}")

    def switch_player(self):
        self.current_player = "yellow" if self.current_player == "red" else "red"

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            for d in (-1, 1):
                r, c = row, col
                while True:
                    r += dr * d
                    c += dc * d
                    if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == self.current_player:
                        count += 1
                    else:
                        break

            if count >= 4:
                return True

        return False

    def reset_game(self):
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = "red"
        self.canvas.delete("piece")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Puissance4()
    game.run()
