#Créé par Alexandre Wilbur en 2023
import enum
class GameState(enum.Enum): #Même chose que pour la classe Attack_TYpe
    GAME_NOT_STARTED = 0
    ROUND_ACTIVE = 1
    ROUND_DONE = 2
    GAME_OVER = 3