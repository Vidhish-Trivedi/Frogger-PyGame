import pygame as pg
pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pg.Surface(size=(50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=position)

        # Float based position
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2((0, 0))
        self.speed = 200

    def move_player(self, deltaTime):
        if(self.direction.magnitude() != 0):
            self.direction = self.direction.normalize()
        self.pos += self.direction*self.speed*deltaTime
        self.rect.center = (round(self.pos.x), round(self.pos.y))


    def input(self):
        keyboard_keys = pg.key.get_pressed()
        # The order of these if/elif/else statements will determine if we can move diagonally or not (Detect simultaneous key presses).
        if(keyboard_keys[pg.K_LEFT]):
            print("Left")
            self.direction.x = -1

        elif(keyboard_keys[pg.K_RIGHT]):
            print("Right")
            self.direction.x = 1
        
        else:
            self.direction.x = 0

        if(keyboard_keys[pg.K_UP]):
            print("Up")
            self.direction.y = -1

        elif(keyboard_keys[pg.K_DOWN]):
            print("Down")
            self.direction.y = 1
        
        else:
            self.direction.y = 0


    def update(self, deltaTime):
        self.input()
        self.move_player(deltaTime)

#################  ADJUST/NORMALIZE A VECTOR (OTHERWISE DIAGONAL SPEED WOULD BE SQRT(V1 + V2))  #####################
# Meaning length of vector should be 1.
#####################################################################################################################
