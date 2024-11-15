import pygame
import time
import random
import csv
import os
import serial  # Import de la bibliothèque pour la communication série
from model.qte_event import QTEEvent
from view.renderer import Renderer

class GameController:
    def __init__(self, player_name, serial_port):
        # Initialisation de Pygame et des variables de la classe
        pygame.init()
        self.player_name = player_name
        self.screen = pygame.display.set_mode((800, 600))
        self.background_image = pygame.image.load('assets/images/background.png').convert()
        self.renderer = Renderer(self.screen, 'assets/images/spritesheet_player.png')
        self.qte_event = None
        self.running = True
        self.paused = False  # Indique si le jeu est en pause
        self.start_time = time.time()  # Heure de début pour calculer la difficulté
        self.next_qte_time = time.time() + random.uniform(2, 4)  # Temps avant le prochain QTE
        self.qte_warning_time = 0.5  # Temps d'avertissement avant le QTE
        self.difficulty_level = 1  # Niveau de difficulté initial
        self.min_interval = 0.5  # Intervalle minimum entre les QTE
        self.score = 0  # Score du joueur
        self.lives = 3  # Nombre de vies du joueur
        self.shake_duration = 0  # Durée de l'effet de tremblement

        # Initialisation de la connexion série avec l'ESP32
        self.serial_connection = None
        if serial_port:
            try:
                self.serial_connection = serial.Serial(serial_port, 115200, timeout=1)
                print(f"Connexion série établie sur le port {serial_port}")
            except serial.SerialException:
                print(f"Impossible de se connecter au port {serial_port}. Le jeu continuera sans l'ESP32.")

        # Initialisation de la musique
        pygame.mixer.init()
        pygame.mixer.music.load('assets/musics/champion_red_battle.mp3')
        pygame.mixer.music.play(-1)

    def trigger_qte(self):
        """Déclenche un nouvel événement de QTE."""
        qte_duration = max(1, 2 - (self.difficulty_level * 0.05))  # Réduit la durée du QTE avec la difficulté
        self.qte_event = QTEEvent(duration=qte_duration)
        self.qte_event.start()

    def update_difficulty(self):
        """Met à jour le niveau de difficulté en fonction du temps écoulé."""
        elapsed_time = time.time() - self.start_time
        self.difficulty_level = int(elapsed_time // 10) + 1  # Augmente le niveau tous les 10 secondes
        interval_range = max(self.min_interval, 4 - (self.difficulty_level * 0.1))
        return interval_range

    def check_defeat(self):
        """Vérifie si le joueur a perdu."""
        return self.lives <= 0

    def apply_shake_effect(self):
        """Applique un effet de tremblement à l'écran."""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            return offset_x, offset_y
        return 0, 0

    def save_score(self):
        """Enregistre le score du joueur dans un fichier CSV."""
        if not os.path.exists('assets/scores.csv'):
            with open('assets/scores.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Pseudo', 'Score', 'Difficulté'])  # Écrire l'en-tête

        with open('assets/scores.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.player_name, self.score, self.difficulty_level])

    def toggle_pause(self):
        """Change l'état de pause du jeu."""
        self.paused = not self.paused

    def check_serial_input(self):
        """Vérifie si un signal de l'ESP32 a été reçu et valide le QTE."""
        if self.serial_connection and self.serial_connection.in_waiting > 0:
            input_data = self.serial_connection.readline().decode().strip()
            if input_data:
                print(f"Données série reçues : {input_data}")
                # Valide le QTE si l'entrée provient d'une touche définie sur l'ESP32
                if input_data in ['U', 'D', 'L', 'R', 'A', 'B', '9']:
                    return True
        return False

    def run(self):
        """Boucle principale du jeu."""
        clock = pygame.time.Clock()
        qte_success_timer = 0
        qte_success_duration = 2  # Durée d'affichage de l'animation de réussite
        show_warning = False

        while self.running:
            dt = clock.tick(60) / 1000  # Temps écoulé depuis la dernière frame

            # Gestion des événements utilisateur
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                        self.toggle_pause()
                    if not self.paused and self.qte_event and self.qte_event.is_active():
                        result = self.qte_event.check_input(event)
                        if result:
                            self.score += 1
                            self.qte_event = None
                            self.renderer.set_qte_success_animation(True)
                            qte_success_timer = time.time()
                        elif result is False:
                            self.lives -= 1
                            self.shake_duration = 15
                            self.qte_event = None

            # Si le jeu est en pause, afficher l'écran de pause
            if self.paused:
                self.screen.blit(self.background_image, (0, 0))
                self.renderer.draw_text("Pause", 350, 300, color=(255, 255, 255))
                self.renderer.draw_text("Appuyez sur Alt pour reprendre", 210, 350, color=(255, 255, 255))
                pygame.display.flip()
                continue  # Passe à la prochaine itération si le jeu est en pause

            # Vérification des données série pour la validation du QTE
            if not self.paused and self.qte_event and self.qte_event.is_active():
                if self.check_serial_input():
                    print("Validation du QTE via l'ESP32")
                    self.score += 1
                    self.qte_event = None
                    self.renderer.set_qte_success_animation(True)
                    qte_success_timer = time.time()

            # Mise à jour du niveau de difficulté et gestion des nouveaux QTE
            interval_range = self.update_difficulty()
            if not self.qte_event and time.time() >= self.next_qte_time - self.qte_warning_time:
                show_warning = True
            if not self.qte_event and time.time() >= self.next_qte_time:
                self.trigger_qte()
                self.next_qte_time = time.time() + random.uniform(interval_range, interval_range + 2)
                show_warning = False

            # Gestion de l'échec du QTE
            if self.qte_event and self.qte_event.has_failed():
                self.lives -= 1
                self.shake_duration = 15
                self.qte_event = None

            # Vérifie si le joueur a perdu
            if self.check_defeat():
                self.renderer.draw_defeat_message()
                pygame.display.flip()
                time.sleep(3)
                self.running = False
                self.save_score()
                return 'menu'

            # Réinitialise l'animation de réussite si nécessaire
            if self.renderer.is_qte_success and time.time() - qte_success_timer > qte_success_duration:
                self.renderer.set_qte_success_animation(False)

            # Applique l'effet de tremblement si activé
            offset_x, offset_y = self.apply_shake_effect()
            self.screen.blit(self.background_image, (offset_x, offset_y))

            # Mise à jour des animations et affichage des éléments de jeu
            self.renderer.update_animation(dt)
            self.renderer.draw_player(352, 250)
            self.renderer.draw_score(self.score)
            self.renderer.draw_difficulty_level(self.difficulty_level)
            self.renderer.draw_lives(self.lives)
            self.renderer.draw_text("ALT : Pause", 20, 560, color=(0, 0, 0))

            # Affichage de l'avertissement et du QTE
            if show_warning:
                self.renderer.draw_qte_warning()
            if self.qte_event:
                self.renderer.draw_qte(self.qte_event)

            pygame.display.flip()

        # Fermeture de la connexion série à la fin du jeu
        if self.serial_connection:
            self.serial_connection.close()
            print("Connexion série fermée")

        pygame.mixer.music.stop()
        pygame.quit()
        return self.score, self.difficulty_level
