"""
fichier : game.py
Auteurs : Baptiste Thomassin
Date de réalisation : 16/12/2024
Objectifs :
Elle gère 
- L'initialisation de la fenêtre du jeu.
- La gestion des objets du jeu et des interactions
- Les mises à jour dynamiques 
- Les interfaces de début et de fin de partie.


"""
import tkinter as tk

class Game:
    """
    Classe principale du jeu. Gère l'initialisation, les mises à jour
    et la logique du jeu, y compris l'affichage, les collisions et le score.
    """

    def __init__(self):
        """
        Initialise la fenêtre du jeu, les objets et les paramètres du jeu.
        
        Objectifs :
        - Créer la fenêtre de jeu.
        - Initialiser les objets du jeu (vaisseau, aliens, defenses, projectiles.).
        """
        self.root = tk.Tk()
        self.root.title("Space Invader - Thomassin Diallo")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="black")
        self.canvas.pack()

         # Charger l'image de fond 
        self.bg_image = tk.PhotoImage(file="images/solar-block.gif")


        #réference 
        self.aliens = []  
        self.defense = Defense(self.canvas)
        self.alien = None
        self.vaisseau = None
        self.collision_manager = CollisionManager(self.canvas)
        self.game_over = False
        self.pv = 3  # Nombre de points de vie
        self.max_pv = 3  # Nombre maximum de PV
        self.bar_width = 200  # Largeur de la barre de vie
        self.bar_height = 30  # Hauteur de la barre de vie
       
        try:
            self.background_photo = tk.PhotoImage(file="images/solar-block.gif")  
            self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        except tk.TclError:
            self.canvas.create_rectangle(0, 0, 600, 600, fill="black")

        self.canvas.create_text(300, 50, text="Space Invader", font=("Helvetica", 40, "bold"), fill="purple")

        # Créer les boutons de l'interface
        self.create_buttons()

    def update_health_bar(self):
        """
        Met à jour l'affichage de la barre de vie en fonction des points de vie restants.
        La barre de vie est dessinée sur le canevas en fonction du nombre actuel de PV du joueur.
        
        Sortie :
            - Efface l'ancienne barre de vie (s'il y en a une).
            - Calcule la nouvelle largeur de la barre de vie en fonction des PV restants.
            - Dessine une nouvelle barre de vie et affiche le texte avec le nombre de PV restants.
        """

        # Effacer l'ancienne barre de vie
        self.canvas.delete("health_bar")

        # Calculer la largeur de la barre de vie en fonction des PV
        life_width = (self.pv / self.max_pv) * self.bar_width
        
        # Dessiner la barre de vie
        self.canvas.create_rectangle(10, 10, 10 + life_width, 10 + self.bar_height,
                                     fill="green", tags="health_bar")
        
        # Ajouter le texte sur la barre de vie
        self.canvas.create_text(10 + self.bar_width / 2, 10 + self.bar_height / 2,
                                text=f"{self.pv} PV", fill="white", tags="health_bar")
        
    def create_buttons(self):
        """
        Crée les boutons du jeu pour démarrer, accéder aux options et quitter.
        """
        start_button = tk.Button(self.root, text="Démarrer", font=("Helvetica", 16), command=self.start_game)
        self.canvas.create_window(300, 150, window=start_button)

        options_button = tk.Button(self.root, text="Options", font=("Helvetica", 16), command=self.open_options)
        self.canvas.create_window(300, 250, window=options_button)

        quit_button = tk.Button(self.root, text="Quitter", font=("Helvetica", 16), command=self.root.quit)
        self.canvas.create_window(300, 350, window=quit_button)

    def start_game(self):
        """
        Démarre une nouvelle partie. Réinitialise le jeu et affiche le vaisseau et les ennemis.
        
        Objectifs :
        - Réinitialiser le jeu (points de vie, score, etc.).
        - Afficher les éléments de départ (vaisseau, ennemis, fond).
        """
        self.game_over = False
        self.canvas.delete("all")
        quitter_button = tk.Button(self.root, text="Quitter", font=("Helvetica", 16), command=self.root.quit)
        self.canvas.create_window(300, 30, window=quitter_button)

        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw") # Afficher l'image de fond
        self.defense.creer_defenses()  # Créer les défenses au démarrage du jeu
        self.alien = Alien(self, self.canvas)

         # Compléter la liste des ennemis
        self.aliens = [self.alien]

        self.vaisseau = Vaisseau(self.canvas, "images/spaceship.png", x=300, y=350)
        self.update_health_bar()
        self.mettre_a_jour()
        self.score=0
        self.score_text = self.canvas.create_text(500, 30, text=f"Score: {self.score}", font=('Arial', 18), fill='white')

    def open_options(self):
        """
        Affiche les options du jeu (options a venir).
        """
        self.canvas.create_text(400, 300, text="Options à venir...", font=("Helvetica", 20), fill="white") 

    def afficher_score(self):
        """
        Affiche le score actuel du joueur à l'écran.
        """
        self.canvas.create_text(300, 30, text=f"Score: {self.score}", font=('Arial', 18), fill='white')

    def incrementer_score(self):
        """
        Incrémente le score du joueur lorsque un alien est détruit.
        """
        self.score += 10  # Ajouter 10 points chaque fois qu'un envahisseur est détruit
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")  # Mise à jour du texte

    def mettre_a_jour(self):
        """
        Met à jour l'état du jeu en fonction des actions des joueurs et des ennemis.
        Gère les déplacements, les collisions, et l'état du jeu (fin, victoire).
        """

        if self.game_over:
            return
        
        self.vaisseau.mettre_a_jour_projectiles()

        # Déplace les projectiles de l'alien et gère leur état
        for alien_projectile in self.alien.aliens_projectiles:
            alien_projectile.deplacer()
            if self.collision_manager.detecter_collision_2(alien_projectile, [self.vaisseau.vaisseau_id]):
            # Collision détectée, on enlève une vie
                self.pv -= 1  # Réduire le nombre de vies
                self.update_health_bar()  # Mettre à jour l'affichage de la barre de vie
                alien_projectile.delete()  # Supprimer le projectile alien
                if self.pv <= 0:
                    self.game_over = True
                    self.afficher_game_over()  # Afficher l'écran de fin de jeu
            # Collision entre le projectile de l'alien et les défenses
            defense_touchee = self.collision_manager.detecter_collision(
            alien_projectile,
            [],  
            self.defense.squares_left + self.defense.squares_right)
            if defense_touchee:
                alien_projectile.delete()

                
           
        
        # Gère les projectiles du vaisseau
        for projectile in self.vaisseau.projectiles:
            if isinstance(projectile, Projectile):
                alien_touche = self.collision_manager.detecter_collision(projectile, self.alien.get_aliens(), self.defense.squares_left + self.defense.squares_right)
            if alien_touche:
                self.incrementer_score()
                self.alien.listaliens.remove(alien_touche)
                projectile.delete()  # Supprime le projectile après la collision
                if self.alien.listaliens==[]:
                    self.afficher_win()

        self.root.after(50, self.mettre_a_jour)
        

    def afficher_game_over(self):
        """
        Affiche un écran de fin de jeu lorsque le joueur a perdu.
        """
        self.canvas.delete("all")
        self.canvas.create_text(300, 100, text="GAME OVER", font=("Helvetica", 40, "bold"), fill="red")
        """ self.canvas.create_text(300, 200, text=f"Votre Score: {self.score}", font=('Arial', 18), fill='white')"""
        rejouer_button = tk.Button(self.root, text="Rejouer", font=("Helvetica", 16), command=self.rejouer)
        quitter_button = tk.Button(self.root, text="Quitter", font=("Helvetica", 16), command=self.root.quit)
        self.canvas.create_window(200, 300, window=rejouer_button)
        self.canvas.create_window(400, 300, window=quitter_button)
    
    def afficher_win(self):
        """
        Affiche un écran de victoire lorsque tous les ennemis sont détruits.
        """
        self.canvas.delete("all")
        self.canvas.create_text(300, 100, text="FELICITATION", font=("Helvetica", 40, "bold"), fill="yellow")
        """self.canvas.create_text(300, 200, text=f"Votre Score: {self.score}", font=('Arial', 18), fill='white')"""
        rejouer_button = tk.Button(self.root, text="Rejouer", font=("Helvetica", 16), command=self.rejouer)
        quitter_button = tk.Button(self.root, text="Quitter", font=("Helvetica", 16), command=self.root.quit)
        self.canvas.create_window(200, 300, window=rejouer_button)
        self.canvas.create_window(400, 300, window=quitter_button)

    def rejouer(self):
        """
        Redémarre le jeu après une victoire ou une défaite.
        """
        self.canvas.delete("all")
        self.alien = None
        self.vaisseau = None
        """self.pv=3"""
        self.start_game()
        