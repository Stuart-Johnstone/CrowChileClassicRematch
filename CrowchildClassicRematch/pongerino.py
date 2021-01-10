import pygame, sys, random,time
#import pygame.locals as gameGlobals,allows a key to be held down to do a repeat action
window =  pygame.display.set_mode((400,500))
pygame.init()
pygame.font.init()
pygame.key.set_repeat(1,10)
#creates the font and size of the text
font = pygame.font.SysFont("Times New Roman", 30)


#some variables
score1 = 0
score2 = 0
timer = 0
screen = "menu"
transition = 3
pwr = False
pwrStor = "none"
aiLvl = ""

#colors for ease of use
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)



class pddl:
    #initalizes the paddle
    def __init__(self,xPos, yPos, color):
        self.xPos = xPos
        self.yPos = yPos
        self.color = color
    #draws the paddles
    def draw(self):
        pygame.draw.rect(window, self.color,(self.xPos,self.yPos,50,10))
    #controlls for paddle 1
    def move1(self,key):
        if key == ",":
            if self.xPos >= 0:
                self.xPos -= 4
        elif key == ".":
            if self.xPos <= 350:
                self.xPos += 4
    #controlls for paddle 2
    def move2(self,key):
        if key == "z" :
            if self.xPos >= 0:
                self.xPos -= 4
        elif key == "x":
            if self.xPos <= 350:
                self.xPos += 4



class circl:
    #initalizes the function
    def __init__(self,xPos, yPos, color):
        self.xPos = xPos
        self.yPos = yPos
        self.color = color
        self.xSpeed = -7
        self.ySpeed = 5
        self.maxSpeed = 8
    #draws the circle
    def draw(self):
        pygame.draw.circle(window, self.color,(self.xPos,self.yPos),25,25)

    def move(self, rec1, rec2):
        #collision for the walls
        if self.xPos in range(375,10000):
            self.xSpeed = -(random.randrange(3,7))
            if self.ySpeed > 0:
                self.ySpeed = random.randrange(6,self.maxSpeed)
            else:
                self.ySpeed = -(random.randrange(6,self.maxSpeed))
        elif self.xPos in range(-10000,25):
            self.xSpeed = random.randrange(3,7)
            if self.ySpeed > 0:
                self.ySpeed = random.randrange(6,self.maxSpeed)
            else:
                self.ySpeed = -(random.randrange(6,self.maxSpeed))

        #collision for the paddles
        if (self.yPos < 70 and self.xPos in range(rec2[0]-25, rec2[0]+75)) or (self.yPos > 450 and self.xPos in range(rec1[0]-25, rec1[0]+75)):
            self.xSpeed = -(self.xSpeed)
            
        elif self.yPos in range(rec1[1]-25, rec1[1]+35) and self.xPos in range(rec1[0]-25, rec1[0]+75):
            self.ySpeed = -(self.ySpeed)

        elif (self.yPos in range(rec2[1]-25, rec2[1]+35)) and (self.xPos in range(rec2[0]-25, rec2[0]+75)):
            self.ySpeed = -(self.ySpeed)

        #moves the ball based on the speed
        self.yPos += self.ySpeed
        self.xPos += self.xSpeed
        self.draw()
    #if the click is with in the hitbox then it will check for the health of the target

class pwrBall(circl):
    #makes the ball green and makes the max speed faster
    def __init__(self,xPos,yPos,xSpeed,ySpeed):
        circl.__init__(self,xPos,yPos,green)
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.color = green
        self.maxSpeed = 12

class pwrSpawn():
    def __init__(self,xPos,yPos,color):
        self.xPos = xPos
        self.yPos = yPos
        self.color = color
    def draw(self):
        pygame.draw.rect(window, self.color,(self.xPos,self.yPos,20,20))
    def col(self,ballX,ballY):
        if ballX in range(self.xPos-25, self.xPos + 45) and ballY in range(self.yPos-25, self.yPos + 45):
            return True
        else:
            return False


    




def scoreCheck(bPos):
     #checks if the ball is out of the screen and gives the point to the other player
    if bPos > 525:
        return "score1"
    elif bPos < -25:
        return "score2"

def onScore():
    #if someone scores then it resets some variables
    ball.xPos = 200
    paddle1.xPos = 175
    paddle2.xPos = 175
    ball.ySpeed = 0
    ball.draw()
    return 1

def ai(aiLvl):
    #moves the paddle based on the ai lvl
    if paddle2.xPos - ball.xPos > 6:
        if paddle2.xPos > 5:
            paddle2.xPos -= aiLvl
    elif paddle2.xPos - ball.xPos < -6:
        if paddle2.xPos < 395:
            paddle2.xPos += aiLvl

def menu():
    textsurface2 = font.render('press 0 for multiplayer' ,True, (0, 0, 0))
    textsurfaceE = font.render('press 1 for a easy ai',True , (0,0,0))
    textsurfaceM = font.render('press 2 for a meduim ai',True , (0,0,0))
    textsurfaceH = font.render('press 3 for a hard ai',True , (0,0,0))
    window.blit(textsurface2,(50,50+25))
    window.blit(textsurfaceE,(50,100+25))
    window.blit(textsurfaceM,(50,150+25))
    window.blit(textsurfaceH,(50,200+25))


        
#makes the targets, gives them random starting cords and random speeds
ball = circl(200,100,red)
paddle1 = pddl(175, 450, blue)
paddle2 = pddl(175, 50, blue)




clock = pygame.time.Clock()
#main function loop
while True:
    clock.tick(60)
    
    #makes the window white
    window.fill(white)
    #needed inorder to allow for keys to be held down

    #blits the menu to the game over screen to re-display the options
    if screen == "menu":
        textsurface = font.render('Pong.... But Again ' ,True, (0, 0, 0))
        window.blit(textsurface,(50,25))
        menu()
        
    elif screen == "transition":

        if transition != 0:
            window.fill(white)
            text = font.render(str(transition),True , (0,0,0))
            window.blit(text,(200,200))
            transition -= 1
            time.sleep(1)

        elif transition == 0:
            screen = "game"
            transition = 3
        
    #game over text, blits the menu to the game over screen to re-display the options
    elif screen == "game over":
        textsurface = font.render('Game over ' ,True, (0, 0, 0))
        window.blit(textsurface,(50,25))
        menu()
        score1 = 0
        score2 = 0
        timer = 0
        pwr = False

    #the main game function
    elif screen == "game":
        #moves the ball
        ball.move((paddle1.xPos,paddle1.yPos),(paddle2.xPos,paddle2.yPos))


        #stops the ball when a point is scored
        time.sleep(timer)
        timer = 0

        #checks to see if anyone won
        if scoreCheck(ball.yPos) == "score1":
            score1 += 1
            ball = circl(ball.xPos,ball.yPos,red)
            ball.yPos = 400
            timer = onScore()
            ball.ySpeed = -6
            pwr = False
            if pwrStor != "none":
                pwrStor.xPos = 10000

        elif scoreCheck(ball.yPos) == "score2":
            score2 += 1
            ball = circl(ball.xPos,ball.yPos,red)
            ball.yPos = 100
            timer = onScore()
            ball.ySpeed = 6
            pwr = False
            if pwrStor != "none":
                pwrStor.xPos = 10000

        # if the ai lvl is over 1 then it will move the paddle to ward the ball
        if aiLvl > 0:
            ai(aiLvl)

            
        if random.randrange(1,1000) == 1 and pwr == False:
            pwrStor = pwrSpawn(random.randrange(100,300),random.randrange(100,400),green)
            pwr = True
        if pwrStor != "none":
            pwrStor.draw()
            pwrStor.col(ball.xPos,ball.yPos)
            if pwrStor.col(ball.xPos,ball.yPos) == True:
                ball = pwrBall(ball.xPos,ball.yPos,ball.xSpeed,ball.ySpeed)
                pwrStor.xPos = 1000000


        fps = font.render('FPS: '+ str(int(clock.get_fps())), True, green)
        window.blit(fps, (300, 5))

        paddle1.draw()
        paddle2.draw()
        #draws the score, updates the display, and allows for multipal key inputs
        textsurface = font.render('Score: ' + str(score1), True, (0, 0, 0))
        textsurface2 = font.render('Score: ' + str(score2), True, (0, 0, 0))
        window.blit(textsurface,(0,5))
        window.blit(textsurface2,(0,480))

        if score1 == 3 or score2 == 3:
            screen = "game over" 



    pygame.display.update()
    #after drawing all of the objs it looks for events
    for event in pygame.event.get():
        #inputs for the game
        if event.type == pygame.KEYDOWN and screen == "game":
            if pygame.key.get_pressed()[pygame.K_COMMA]:
                paddle1.move1(",")
            if pygame.key.get_pressed()[pygame.K_PERIOD]:
                paddle1.move1(".")
            if pygame.key.get_pressed()[pygame.K_z] and aiLvl == 0:
                paddle2.move2("z")
            if pygame.key.get_pressed()[pygame.K_x] and aiLvl == 0:
                paddle2.move2("x")
        if event.type == pygame.KEYDOWN and (screen == "menu" or  screen == "game over"):
            if event.key == pygame.K_0:
                aiLvl = 0
                screen = "transition"
            elif event.key == pygame.K_1:
                aiLvl = 4
                screen = "transition"
            elif event.key == pygame.K_2:
                aiLvl = 5
                screen = "transition"
            elif event.key == pygame.K_3:
                aiLvl = 6
                screen = "transition"
        #quits pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()