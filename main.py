#Créé par Alexandre Wilbur en 2023 et en 2024

import random, arcade, attack_animation, game_state 
#random pour l'hasard du l'attaque de l'ordi, attack_animation et game_state sont les autres fichiers

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # The default line height for text.
POSSIBLE_ATTACKS = [attack_animation.AttackType.ROCK, attack_animation.AttackType.SCISSORS, attack_animation.AttackType.PAPER]

class MyGame(arcade.Window): #la classe princiaple (la fenêtre qui s'ouvre)
   def __init__(self, width, height, title): 
      super().__init__(width, height, title) #Initialiser la fenêtre arcade.Window

      arcade.set_background_color(arcade.color.BLACK_OLIVE)

      self.static_sprites = arcade.SpriteList() #La liste spécialisée qui va contenir chaque sprite de joueur
      self.static_sprites.append(sprite=arcade.Sprite("assets\gfaceBeard.png", 0.4, center_x = (SCREEN_WIDTH / 4), center_y = SCREEN_HEIGHT / 4))    
      self.static_sprites.append(sprite=arcade.Sprite("assets\compy.png", 2, center_x = (SCREEN_WIDTH / 4)*3, center_y = SCREEN_HEIGHT / 4))
      
      self.reset_round() #Mettre la majorité de nos variables à leur valeurr de départ

      self.game_state = game_state.GameState.GAME_NOT_STARTED #On commence à (not started)
      self.pointage_usager, self.pointage_ordi = 0, 0
      self.winner = "undetermined"

   def validate_victory(self, chosen_attack, computer_attack): #On veut trouver qui a gagné à partir de l'attaque choisie et de l'attaque de l'ordi
      #Wining cases for player
      if chosen_attack.attack_type == attack_animation.AttackType.SCISSORS and computer_attack.attack_type == attack_animation.AttackType.PAPER:
         self.pointage_usager += 1
         return "player"
      
      if chosen_attack.attack_type == attack_animation.AttackType.PAPER and computer_attack.attack_type == attack_animation.AttackType.ROCK:
         self.pointage_usager += 1
         return "player"

      if chosen_attack.attack_type == attack_animation.AttackType.ROCK and computer_attack.attack_type == attack_animation.AttackType.SCISSORS:
         self.pointage_usager += 1
         return "player"
      
      #Wining cases for the "computer"
      if computer_attack.attack_type == attack_animation.AttackType.SCISSORS and chosen_attack.attack_type == attack_animation.AttackType.PAPER:
         self.pointage_ordi += 1
         return "computer"
         
      if computer_attack.attack_type == attack_animation.AttackType.PAPER and chosen_attack.attack_type == attack_animation.AttackType.ROCK:
         self.pointage_ordi += 1
         return "computer"

      if computer_attack.attack_type == attack_animation.AttackType.ROCK and chosen_attack.attack_type == attack_animation.AttackType.SCISSORS:
         self.pointage_ordi += 1
         return "computer"
      
      return "draw"
   
   def draw_possible_attack(self): #Animer et dessiner tous les attaques, qui sont des objets de la classe Attack_Animation

      #L'avantage qui vient en utilisant des variables pour la méthode on_update() et on_draw() de chaque attaque,
      # donc 4 x 2 = 8 variables, est de pouvoir facilement arrêter l'animation ou le dessin de chaque atttaque(4 attaques)
      #d'une manière INDÉPENDANTE
   
      if self.animate_paper: self.paper.on_update()

      if self.draw_paper: self.paper.draw()

      if self.animate_rock: self.rock.on_update()

      if self.draw_rock: self.rock.draw()

      if self.animate_scissor: self.scissor.on_update()

      if self.draw_scissor: self.scissor.draw()

      if self.animate_computer_attacks: self.computer_attack.on_update()

      if self.draw_computer_attacks: self.computer_attack.draw()

   def draw_miscellaneous_things(self): #Dessiner les éléments qui ne bougent pas
      
      #Les pointages avec les 2 varibles de pointage comme paramètre de texte
      arcade.draw_text("Pointage de l'usager %s"%self.pointage_usager,0,SCREEN_HEIGHT / 12,arcade.color.FLORAL_WHITE,30,width=SCREEN_WIDTH)
      arcade.draw_text("Pointage de l'ordi %s"%self.pointage_ordi,600,SCREEN_HEIGHT / 12,arcade.color.FLORAL_WHITE,30,width=SCREEN_WIDTH)
      
      arcade.draw_text("VS",0,SCREEN_HEIGHT /2- DEFAULT_LINE_HEIGHT*2,arcade.color.BLACK_BEAN,40,width=SCREEN_WIDTH,align="center")

      self.static_sprites.draw() #Les 2 sprites de joueurs

      #Draw Attack boxes
      arcade.draw_rectangle_outline(center_x=(SCREEN_WIDTH/4)-100, center_y=SCREEN_HEIGHT/2, width=80, height=80, color=arcade.color.BLACK_BEAN, border_width=2)
      arcade.draw_rectangle_outline(center_x=SCREEN_WIDTH/4, center_y=SCREEN_HEIGHT/2, width=80, height=80, color=arcade.color.BLACK_BEAN, border_width=2)
      arcade.draw_rectangle_outline(center_x=(SCREEN_WIDTH/4)+100, center_y=SCREEN_HEIGHT/2, width=80, height=80, color=arcade.color.BLACK_BEAN, border_width=2)
      
      arcade.draw_rectangle_outline(center_x=(SCREEN_WIDTH/4)*3, center_y=SCREEN_HEIGHT/2, width=80, height=80, color=arcade.color.BLACK_BEAN, border_width=2)

   def on_draw(self): #Dessiner les éléments selon l'état du jeu (GameState)
      arcade.start_render()
        
      if self.game_state == game_state.GameState.GAME_NOT_STARTED:
         
         arcade.draw_text(SCREEN_TITLE,0,SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,arcade.color.BLACK_BEAN,60,width=SCREEN_WIDTH,align="center")
         arcade.draw_text("Appuie sur espace pour commencer",0,SCREEN_HEIGHT /2- DEFAULT_LINE_HEIGHT*2,arcade.color.BLACK_BEAN,40,width=SCREEN_WIDTH,align="center")

      elif self.game_state == game_state.GameState.ROUND_ACTIVE:
         
         #Draw Attack Animations

         if self.animate_attacks: self.draw_possible_attack() #choses qui changent
         
         arcade.draw_text("Appuyer sur une image \npour faire une attaque!",0,SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,arcade.color.FLORAL_WHITE,60,width=SCREEN_WIDTH,align="center")

         self.draw_miscellaneous_things() #choses qui changent pas
         

      elif self.game_state == game_state.GameState.ROUND_DONE:
         if self.winner == "player":
            arcade.draw_text("Bravo! Vous-avez gagné!\nAppuyer sur 'ESPACE' pour démarrer une nouvelle ronde",0,SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,arcade.color.FLORAL_WHITE,40,width=SCREEN_WIDTH,align="center")
         
         elif self.winner == "computer":
            arcade.draw_text("Womp Womp... L'ordi a gagné!\nAppuyer sur 'ESPACE' pour démarrer une nouvelle ronde",0,SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,arcade.color.FLORAL_WHITE,40,width=SCREEN_WIDTH,align="center")
         
         elif self.winner == "draw":
            arcade.draw_text("Womp Womp... C'est une ronde nulle...\nAppuyer sur 'ESPACE' pour démarrer une nouvelle ronde",0,SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,arcade.color.FLORAL_WHITE,40,width=SCREEN_WIDTH,align="center")
            
         self.draw_miscellaneous_things() #choses qui changent pas

         #Draw Attack Animations

         if self.animate_attacks: self.draw_possible_attack()#choses qui ne changent pas

      elif self.game_state == game_state.GameState.GAME_OVER: #Puisqu'on est à l'état GAME_OVER parce que un des pointages est monté à 3, on peux simplement dire ceci:
         
         if self.pointage_usager == 3: arcade.draw_text("Bravo! Vous avez gagné la partie! Merci pour avoir joué!\nAppuyer sur 'ESPACE' pour démarrer une nouvelle partie",0,SCREEN_HEIGHT / 2,arcade.color.FLORAL_WHITE,40,width=SCREEN_WIDTH,align="center")
         elif self.pointage_ordi == 3: arcade.draw_text("Womp Womp... Vous avez perdu...(skill issue) Merci pour avoir joué!\nAppuyer sur 'ESPACE' pour démarrer une nouvelle partie",0,SCREEN_HEIGHT / 2,arcade.color.FLORAL_WHITE,40,width=SCREEN_WIDTH,align="center")
   
   def on_update(self, delta_time):

      if self.computer_attack.nmb_of_swaps == 5: 
         #On veux attendre que l'attaque de l'ordi (roule) pendant 5 swap pour créer du suspense...
         #on n'attend pas avec time.sleep(), mais avec le delta_time du on_update de l'autre classe (voir l'autre fichier)

         #Changer computre_attack à le bon Attack_Type qui est aléatoire grâce au random.choice()
         #et arrêter de l'animer pour faire comprendre à l'usager quel attaque l'ordi a prit

         self.computer_attack = attack_animation.AttackAnimation(random.choice(POSSIBLE_ATTACKS), SCREEN_WIDTH*0.75, SCREEN_HEIGHT/2)
         self.animate_computer_attacks = False

         #Deciding who wins
         self.winner = self.validate_victory(self.chosen_attack, self.computer_attack)

         self.game_state = game_state.GameState.ROUND_DONE #La ronde est terminée

         if self.pointage_usager == 3 or self.pointage_ordi == 3:# SI la partie est terminée
            self.game_state = game_state.GameState.GAME_OVER

   def on_key_press(self, key, key_modifiers):

      if key == 32 and self.game_state == game_state.GameState.GAME_NOT_STARTED: #On passe toujours de NOT_STARTED à ROUND_ACTIVE, quand on appuie sur espace(32)
         
         self.game_state = game_state.GameState.ROUND_ACTIVE
         
      if key == 32 and self.game_state == game_state.GameState.ROUND_DONE: #On passe toujours de ROUND_DONE à ROUND_ACTIVE et on reset_round(), quand on appuie sur espace(32)

         self.game_state = game_state.GameState.ROUND_ACTIVE
         self.reset_round()
      if key == 32 and self.game_state == game_state.GameState.GAME_OVER: #On passe toujours de GAME_OVER à GAME_NOT_STARTED et on reset_round(), quand on appuie sur espace(32)

         self.game_state = game_state.GameState.GAME_NOT_STARTED
         self.reset_round()
         self.pointage_usager, self.pointage_ordi = 0, 0
         self.winner = "undetermined"
   def reset_round(self): #La méthode qui sert à mettre ou à remettre nos variables à la bonne valeur pour faire fonctionner UNE ronde
      
      self.scissor = attack_animation.AttackAnimation(attack_animation.AttackType.SCISSORS, pos_x=SCREEN_WIDTH / 4, pos_y=SCREEN_HEIGHT/2)
      self.rock = attack_animation.AttackAnimation(attack_animation.AttackType.ROCK, pos_x=(SCREEN_WIDTH / 4)-100, pos_y=SCREEN_HEIGHT/2)
      self.paper = attack_animation.AttackAnimation(attack_animation.AttackType.PAPER, pos_x=(SCREEN_WIDTH / 4)+100, pos_y=SCREEN_HEIGHT/2)
      
      #IMPORTANT, en re-déclarant computer_attack, la variable nmb_of_swap retourne à 0
      #Sinon, le jeu serait stuck entre la phase ou on décide la gagnant et on passe à ROUND_DONE
      self.computer_attack = attack_animation.AttackAnimation(attack_type=attack_animation.AttackType.COMPUTER, pos_x=SCREEN_WIDTH*0.75, pos_y=SCREEN_HEIGHT/2)

      self.animate_attacks = True
      self.animate_paper, self.draw_paper = True, True
      self.animate_scissor, self.draw_scissor = True, True
      self.animate_rock, self.draw_rock = True, True
      self.animate_computer_attacks, self.draw_computer_attacks = False, False

      self.chosen_attack = None

      self.has_chosen_attack = False
   def on_mouse_press(self, x, y, button, key_modifiers): #La fonction qui s'active quand on click dans le jeu
      #On s'assure que la joueur click dans le bon endroit. On s'assure qui n'a pas déja cliqué. On s'assure qu'il clique quand la jeu est ROUND_ACTIVE
      if self.has_chosen_attack == False and self.game_state == game_state.GameState.ROUND_ACTIVE  and (self.rock.collides_with_point((x, y)) or self.paper.collides_with_point((x, y)) or self.scissor.collides_with_point((x, y))): 
         
         self.has_chosen_attack == True #On a déja choisit une attaque

         #Ces trois ifs font tous la même chose:
         #On arrête d'animer et de dessiner les 2 autres attaques. On arrête d'animer l'attaque choisie. On définit chosen_attack comme la Sprite qu'on a cliqu sur
         if self.rock.collides_with_point((x, y)):

            self.animate_paper, self.draw_paper = False, False
            self.animate_scissor, self.draw_scissor = False, False

            self.animate_rock = False
            
            self.chosen_attack = self.rock


         elif self.paper.collides_with_point((x, y)):

            self.animate_rock, self.draw_rock = False, False
            self.animate_scissor, self.draw_scissor = False, False

            self.animate_paper = False

            self.chosen_attack = self.paper

         elif self.scissor.collides_with_point((x, y)):

            self.animate_rock, self.draw_rock = False, False
            self.animate_paper, self.draw_paper = False, False
         
            self.animate_scissor = False

            self.chosen_attack = self.scissor

         #On commence à dessiner et à animer l'attaque de l'ordi, ce qui commence à changer la variable nmb_of_swaps, ce qui va faire progresser la jeu
         self.animate_computer_attacks = True
         self.draw_computer_attacks = True

def main():
   
   game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
   game.on_draw()
   arcade.run() #Avec ces 2 fonctions, on run toujours la méthode on_draw() (qu'on appèle) et la fonction on_update(), même si on l'a pas écrit

if __name__ == "__main__": #pas moi qu'il la écrit
   main()
