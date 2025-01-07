import tkinter as tk
import random

class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird")

        # Canvas setup
        self.canvas = tk.Canvas(root, width=400, height=600, bg="skyblue")
        self.canvas.pack()

        # Game variables
        self.bird = self.canvas.create_oval(50, 250, 90, 290, fill="yellow", outline="black")
        self.bird_velocity = 0
        self.gravity = 2
        self.lift = -10

        self.pipes = []
        self.pipe_speed = 5
        self.pipe_gap = 150

        self.score = 0
        self.score_text = self.canvas.create_text(200, 50, text=f"Score: {self.score}",
                                                  font=("Arial", 24), fill="white")

        # Game state
        self.game_over = False

        # Key bindings
        self.root.bind("<space>", self.flap)

        # Start game loop
        self.spawn_pipe()
        self.update_game()

    def flap(self, event):
        if not self.game_over:
            self.bird_velocity = self.lift

    def spawn_pipe(self):
        if self.game_over:
            return

        pipe_height = random.randint(100, 400)
        top_pipe = self.canvas.create_rectangle(400, 0, 450, pipe_height, fill="green")
        bottom_pipe = self.canvas.create_rectangle(400, pipe_height + self.pipe_gap, 450, 600, fill="green")

        self.pipes.append((top_pipe, bottom_pipe))
        self.root.after(2000, self.spawn_pipe)

    def update_game(self):
        if self.game_over:
            self.canvas.create_text(200, 300, text="Game Over!", font=("Arial", 36), fill="red")
            return

        # Bird physics
        self.bird_velocity += self.gravity
        self.canvas.move(self.bird, 0, self.bird_velocity)

        bird_coords = self.canvas.coords(self.bird)

        # Check for collisions with the top or bottom
        if bird_coords[1] <= 0 or bird_coords[3] >= 600:
            self.end_game()

        # Move pipes and check for collisions
        for top_pipe, bottom_pipe in self.pipes:
            self.canvas.move(top_pipe, -self.pipe_speed, 0)
            self.canvas.move(bottom_pipe, -self.pipe_speed, 0)

            top_coords = self.canvas.coords(top_pipe)
            bottom_coords = self.canvas.coords(bottom_pipe)

            # Check for collision with pipes
            if self.check_collision(bird_coords, top_coords) or self.check_collision(bird_coords, bottom_coords):
                self.end_game()

            # Update score if bird passes a pipe
            if top_coords[2] < 50 and not self.game_over:
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

        # Remove pipes that are off-screen
        self.pipes = [(t, b) for t, b in self.pipes if self.canvas.coords(t)[2] > 0]

        # Schedule next frame
        self.root.after(30, self.update_game)

    def check_collision(self, bird, pipe):
        return not (bird[2] < pipe[0] or bird[0] > pipe[2] or bird[3] < pipe[1] or bird[1] > pipe[3])

    def end_game(self):
        self.game_over = True

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBirdGame(root)
    root.mainloop()
    