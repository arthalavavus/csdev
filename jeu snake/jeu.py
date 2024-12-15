import tkinter as tk
import random

# Définir les couleurs
BLANC = "#FFFFFF"
NOIR = "#000000"
ROUGE = "#D55050"
VERT = "#00FF00"
BLEU = "#32A1C2"

# Définir les paramètres du jeu
LARGEUR = 600
HAUTEUR = 400
TAILLE_BLOC = 10
VITESSE_SNAKE = 100  # Millisecondes entre chaque mouvement

class JeuSnake:
    def __init__(self, master):
        self.master = master
        self.master.title("Jeu Snake")

        # Créer un canvas pour dessiner
        self.canvas = tk.Canvas(self.master, width=LARGEUR, height=HAUTEUR, bg=BLEU)
        self.canvas.pack()

        # Initialiser le serpent
        self.snake = [(LARGEUR // 2, HAUTEUR // 2)]
        self.direction = "DROITE"
        self.length = 1

        # Générer la nourriture
        self.food = self.generer_nourriture()

        # Afficher le score
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Arial", 14))
        self.score_label.pack()

        # Lancer le jeu
        self.game_over = False
        self.mouvement()

        # Lier les touches directionnelles
        self.master.bind("<Left>", self.changer_direction)
        self.master.bind("<Right>", self.changer_direction)
        self.master.bind("<Up>", self.changer_direction)
        self.master.bind("<Down>", self.changer_direction)

    def changer_direction(self, event):
        """Changer la direction du serpent selon la touche appuyée"""
        if event.keysym == "Left" and self.direction != "DROITE":
            self.direction = "GAUCHE"
        elif event.keysym == "Right" and self.direction != "GAUCHE":
            self.direction = "DROITE"
        elif event.keysym == "Up" and self.direction != "BAS":
            self.direction = "HAUT"
        elif event.keysym == "Down" and self.direction != "HAUT":
            self.direction = "BAS"

    def generer_nourriture(self):
        """Générer une position aléatoire pour la nourriture"""
        x = random.randint(0, (LARGEUR - TAILLE_BLOC) // TAILLE_BLOC) * TAILLE_BLOC
        y = random.randint(0, (HAUTEUR - TAILLE_BLOC) // TAILLE_BLOC) * TAILLE_BLOC
        return (x, y)

    def mouvement(self):
        """Gérer le déplacement du serpent"""
        if self.game_over:
            self.canvas.create_text(LARGEUR / 2, HAUTEUR / 2, text="GAME OVER", fill=ROUGE, font=("Arial", 24))
            return

        # Déplacer le serpent
        x, y = self.snake[0]
        if self.direction == "DROITE":
            x += TAILLE_BLOC
        elif self.direction == "GAUCHE":
            x -= TAILLE_BLOC
        elif self.direction == "HAUT":
            y -= TAILLE_BLOC
        elif self.direction == "BAS":
            y += TAILLE_BLOC

        # Ajouter la nouvelle position de la tête
        nouvelle_tete = (x, y)
        self.snake = [nouvelle_tete] + self.snake[:-1]

        # Vérifier la collision avec les murs ou le serpent lui-même
        if x < 0 or x >= LARGEUR or y < 0 or y >= HAUTEUR or nouvelle_tete in self.snake[1:]:
            self.game_over = True
            self.mouvement()  # Re-afficher GAME OVER et arrêter le jeu

        # Vérifier la collision avec la nourriture
        if nouvelle_tete == self.food:
            self.snake.append(self.snake[-1])  # Ajouter un bloc au serpent
            self.length += 1
            self.food = self.generer_nourriture()  # Générer une nouvelle nourriture
            self.score_label.config(text=f"Score: {self.length - 1}")

        # Rafraîchir le canvas
        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + TAILLE_BLOC, segment[1] + TAILLE_BLOC, fill=NOIR)

        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + TAILLE_BLOC, self.food[1] + TAILLE_BLOC, fill=VERT)

        # Appeler la fonction de mouvement après un délai pour créer un effet de "jeu en cours"
        self.master.after(VITESSE_SNAKE, self.mouvement)

# Créer la fenêtre principale avec tkinter
root = tk.Tk()

# Démarrer le jeu
jeu = JeuSnake(root)

# Lancer la boucle principale
root.mainloop()
