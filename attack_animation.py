#Créé par Alexandre Wilbur en 2023

import random, arcade, colorama, time,enum

class AttackType(enum.Enum): #La classe dérive de Enum, qui sert juste à faciliter la lecture du code, parce qu'on voit en lettre majuscules l'attaque
    ROCK = 1,
    PAPER= 2,
    SCISSORS = 3, 
    COMPUTER = 4

class AttackAnimation(arcade.Sprite):
    ATTACK_SCALE = 0.50
    ANIMATION_SPEED = 2.0
    
    def __init__(self, attack_type, pos_x, pos_y): #On prend comme arguement la bonne attaque et la position du Sprite, qu'on passe dans la prochaine ligne
        super().__init__(center_x=pos_x, center_y=pos_y)
        
        self.animation_update_time = 1.0 / AttackAnimation.ANIMATION_SPEED
        self.time_since_last_swap = 0.0
        self.attack_type = attack_type
        
        self.nmb_of_swaps = 0

        #self.texures est une variable liste de la classe parent arcade.SPrite, et elle contient les addresses locales de chaque image nécessaire à l'animation
        
        #On ajoute les bonnes images à cette variable selon le type d'attaque

        if self.attack_type == AttackType.ROCK:
            self.textures = [
                arcade.load_texture("assets/srock.png"),
                arcade.load_texture("assets/srock-attack.png"),
        ]
        elif self.attack_type == AttackType.PAPER:
            self.textures = [
                arcade.load_texture("assets/spaper.png"),
                arcade.load_texture("assets/spaper-attack.png"),
        ]
        elif self.attack_type == AttackType.SCISSORS:
            self.textures = [
                arcade.load_texture("assets/scissors.png"),
                arcade.load_texture("assets/scissors-close.png"),
        ]
        else:
            self.textures = [
                arcade.load_texture("assets/scissors.png"),
                arcade.load_texture("assets/spaper.png"),
                arcade.load_texture("assets/srock-attack.png")
        ]

        self.scale = self.ATTACK_SCALE
        self.current_texture = 0
        self.set_texture(self.current_texture)#On met la première texture
        
    def on_update(self, delta_time = 1/60): #Ici on dit à notre code de se faire 60 fois par seconde
    
        # Update the animation.
        self.time_since_last_swap += delta_time #On ajoute le temps écoulé du delta_time à une variable

        #et quand cette variable représente plus de temps que le temps nécessaire à ce qu'on passe à une nouvelle texture
        if self.time_since_last_swap > self.animation_update_time: 
            #Changer de texture
            self.nmb_of_swaps += 1

            #Dans le fond, chaque texture a un nombre qui le représente, donc de 0 à 2 ou 3 dans notre cas
            self.current_texture += 1 #En augmentant cette variable, on dit de passer à la prochaine texture

            if self.current_texture < len(self.textures): #On s'assure qu'on n'est pas déja à la dernière texture dans la liste
                self.set_texture(self.current_texture) #Si oui, on change la texure à la procahine

            else: #Sinon:
                self.current_texture = 0 #On revient à la première texture (une boucle)
                self.set_texture(self.current_texture)

            self.time_since_last_swap = 0.0 # Et on remet à 0 la temps depuis le swap, puisqu'on vient juste de le faire 