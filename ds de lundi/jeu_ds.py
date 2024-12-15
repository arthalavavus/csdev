"""
fichier : jeu.py
Auteurs : Baptiste Thomassin
Date de réalisation : 16/12/2024
Objectifs : Point d'entrée principal pour le jeu
"""

from game_ds import Game

class Jeu:
    """
    Classe principale pour lancer le jeu 

    Méthodes :
    - lancer() : Initialise et démarre la boucle principale du jeu.
    """

    def lancer():
        """
        Initialise et lance le jeu.

        Entrées : Aucune
        Sorties : Aucune
        """
        game = Game()    # Instance principale du jeu
        game.root.mainloop()    # Démarre la boucle principale de l'interface utilisateur

# Point d'entrée principal
if __name__ == "__main__":
    Jeu.lancer()
