import tkinter as tk
import random

# Paramètres du jeu
TAILLE_GRILLE = 8  # Taille de la grille (8x8)
NOMBRE_MINES = 10  # Nombre de mines

class Demineur:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")

        self.grille = self.creer_grille_vide()
        self.grille_revelee = [['#' for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]
        self.boutons = {}
        self.game_over = False
        self.cases_restantes = TAILLE_GRILLE * TAILLE_GRILLE - NOMBRE_MINES

        # Créer un cadre pour la grille de boutons
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Placer les mines et calculer les voisins
        self.placer_mines()
        self.calculer_voisins()

        # Créer les boutons représentant la grille
        self.creer_boutons()

    def creer_grille_vide(self):
        """ Crée une grille vide de taille TAILLE_GRILLE x TAILLE_GRILLE. """
        return [[' ' for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]

    def placer_mines(self):
        """ Place les mines sur la grille. """
        mines_places = 0
        while mines_places < NOMBRE_MINES:
            x = random.randint(0, TAILLE_GRILLE - 1)
            y = random.randint(0, TAILLE_GRILLE - 1)
            if self.grille[x][y] != 'M':
                self.grille[x][y] = 'M'
                mines_places += 1

    def calculer_voisins(self):
        """ Calcule le nombre de mines autour de chaque case. """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x in range(TAILLE_GRILLE):
            for y in range(TAILLE_GRILLE):
                if self.grille[x][y] == 'M':
                    continue
                count = 0
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < TAILLE_GRILLE and 0 <= ny < TAILLE_GRILLE and self.grille[nx][ny] == 'M':
                        count += 1
                self.grille[x][y] = str(count) if count > 0 else ' '

    def creer_boutons(self):
        """ Crée des boutons sur le canvas représentant la grille. """
        for x in range(TAILLE_GRILLE):
            for y in range(TAILLE_GRILLE):
                bouton = tk.Button(self.frame, width=4, height=2, command=lambda x=x, y=y: self.reveler_case(x, y))
                bouton.grid(row=x, column=y, padx=2, pady=2)
                self.boutons[(x, y)] = bouton

    def reveler_case(self, x, y):
        """ Révèle une case sur la grille. """
        if self.game_over:
            return
        if self.grille[x][y] == 'M':
            self.boutons[(x, y)].config(text='M', background='red')
            self.game_over = True
            self.fin_partie()
        else:
            self.boutons[(x, y)].config(text=self.grille[x][y], background='lightgray')
            self.cases_restantes -= 1
            if self.cases_restantes == 0:
                self.gagner_partie()

    def fin_partie(self):
        """ Affiche un message de fin de partie. """
        for x in range(TAILLE_GRILLE):
            for y in range(TAILLE_GRILLE):
                if self.grille[x][y] == 'M':
                    self.boutons[(x, y)].config(text='M', background='red')
                else:
                    self.boutons[(x, y)].config(state='disabled')
        self.afficher_message("Game Over")

    def gagner_partie(self):
        """ Affiche un message de victoire. """
        for bouton in self.boutons.values():
            bouton.config(state='disabled')
        self.afficher_message("You Win!")

    def afficher_message(self, message):
        """ Affiche un message sur la fenêtre après la fin du jeu. """
        message_label = tk.Label(self.root, text=message, font=('Helvetica', 16))
        message_label.pack()

# Initialisation de la fenêtre principale
root = tk.Tk()

# Lancer le jeu
jeu = Demineur(root)

# Lancer la boucle principale
root.mainloop()
