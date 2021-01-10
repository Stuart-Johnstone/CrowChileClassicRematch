import pygame, sys, random,time
#import pygame.locals as gameGlobals,allows a key to be held down to do a repeat action
window =  pygame.display.set_mode((1500,900))
window.set_alpha(None)
pygame.init()
pygame.font.init()
pygame.key.set_repeat(1,10)
pygame.DOUBLEBUF

#loading backgound images
background = pygame.image.load("background.png")
calBackground = pygame.image.load("uofcloses.png")
mruBackground = pygame.image.load("mruloses.png")
#loading the player images
d = pygame.image.load("dinosupercoolman.png")
dPunch = pygame.image.load("New_Piskel.png")
c = pygame.image.load("cougaMan.png")
cPunch = pygame.image.load("cougaManArm.png")


#creates the font and size of the text
font = pygame.font.SysFont("Times New Roman", 30)
textMRU = font.render("MRU Cougar",True , (0,0,0))
textZ = font.render("Z: Left",True , (0,0,0))
textX = font.render("X: Right",True , (0,0,0))
textQ = font.render("Q: Punch",True , (0,0,0))

textCal = font.render("UofC Dino",True , (0,0,0))
textL = font.render("<: Left",True , (0,0,0))
textR = font.render(">: Right",True , (0,0,0))
textP = font.render("P: Punch",True , (0,0,0))

#some variables
timer = 0
screen = "menu"
transition = 3

#colors for ease of use
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)

#The general class for the player
class Player():
    def __init__(self,xPos,xRange,yPos,pPos,pyPos,healthX,img,fist,uni):
        self.health = 4.0
        self.xPos = xPos
        self.xRange = xRange
        self.yPos = yPos
        self.pPos = pPos
        self.pyPos = pyPos
        self.img = img
        self.fist = fist
        self.healthX = healthX      #stors the enemies health
        self.uni = uni
    #draws the character and the opponents health
    def draw(self):
        window.blit(self.img, (self.xPos, self.yPos))
        textsurface2 = font.render(str(self.health),True, (0, 0, 0))
        window.blit(textsurface2,(self.healthX,100))

    #moves the character left
    def moveLeft(self,obj):
        if(self.xPos > 100):
            self.xPos -= 50
    #moves the character right
    def moveRight(self,obj):
        if(self.xPos < 1400):
            self.xPos += 50

    #this section  displays the fist and checks if the player is hit
    def Punch(self,objX,objRange):
        window.blit(self.fist, (self.xPos + self.pPos, self.yPos + self.pyPos))

        #this if statement changes  
        if(self.xPos < (objX + objRange) and self.xPos > objX):
            self.health = score(self.health,self.uni)

        #different x cord dectetion for the other university
        elif (self.xPos > (objX + objRange) and self.xPos < objX):
            self.health = score(self.health,self.uni)

#this score function deals with doing damage and changing to the end screen for each university
def score(h,u):
    global screen
    GPAs = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0]
    current = GPAs.index(h)
    next = current + 1
    if (GPAs[next] < 1):
        if u == "uCal":
            screen = "uCal"
            return GPAs[next]
        else:
            screen = "mrUwU"
            return GPAs[next]
    else:
        return GPAs[next]

#initalizes the players
player1 = Player(1000,-400,400,-100,-40,100,d,dPunch,"uCal")
player2 = Player(100,400,400,120,-20,1400,c,cPunch,"mrUwU")

clock = pygame.time.Clock()
#main function loop
while True:
    clock.tick(30)
    
    #makes the window white
    window.fill(white)
    #needed inorder to allow for keys to be held down

    #blits the menu background
    if screen == "menu":
        window.blit(background,(0,0))
        
    elif screen == "transition":

        if transition != 0:
            window.fill(white)
            text = font.render(str(transition),True , (0,0,0))
            window.blit(text,(750,450))

            window.blit(textMRU,(100,100))
            window.blit(textZ,(100,130))
            window.blit(textX,(100,160))
            window.blit(textQ,(100,190))

            window.blit(textCal,(1300,100))
            window.blit(textL,(1300,130))
            window.blit(textR,(1300,160))
            window.blit(textP,(1300,190))

            transition -= 1
            time.sleep(1)

        elif transition == 0:
            screen = "game"
            transition = 3
        
    #game over screen for ucalgary
    elif screen == "uCal":
        window.blit(mruBackground,(0,0))

    #game over screen for mru
    elif screen == "mrUwU":
        window.blit(calBackground,(0,0))

    #main game loop
    elif screen == "game":
        player1.draw()
        player2.draw()




    #after drawing all of the objs it looks for events
    for event in pygame.event.get():
        #inputs for the game
        if event.type == pygame.KEYDOWN and screen == "game":
            if event.key == pygame.K_p:
                player1.Punch(player2.xPos,player2.xRange)
            if pygame.key.get_pressed()[pygame.K_COMMA]:
                player1.moveLeft(player2)
            if pygame.key.get_pressed()[pygame.K_PERIOD]:
                player1.moveRight(player2)
            if pygame.key.get_pressed()[pygame.K_q]:
                player2.Punch(player1.xPos,player1.xRange)
            if pygame.key.get_pressed()[pygame.K_z]:
                player2.moveLeft(player2)
            if pygame.key.get_pressed()[pygame.K_x]:
                player2.moveRight(player2)
        if event.type == pygame.KEYDOWN and (screen == "menu" or  screen == "game over"):
            if event.key == pygame.K_RETURN:
                screen = "transition"
        #quits pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()