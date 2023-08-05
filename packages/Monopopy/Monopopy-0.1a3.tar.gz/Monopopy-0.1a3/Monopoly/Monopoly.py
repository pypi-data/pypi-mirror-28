#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Title: Monopoly
# Author: Ryan J. Slater
# Date: 12/28/2017
# =============================================================================

import pygame
import random as rand

class colors():
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (200,0,0)
    GREEN = (0,200,0)
    BLUE = (0, 0, 200)
    BRIGHTRED = (255,0,0)
    BRIGHTGREEN = (0,255,0)
    BRIGHTBLUE = (0, 0, 255)
    PURPLE = (78, 0, 107)
    LIGHTBLUE = (0, 187, 233)
    PINK = (179, 0, 161)
    ORANGE = (228, 91, 0)
    YELLOW = (255, 255, 0)
    DARKGREEN = (0, 102, 0)
    DARKBLUE = (0, 0, 102)

    def getPropertyColor(color):
        if color == 'purple':
            return colors.PURPLE
        elif color == 'light blue':
            return colors.LIGHTBLUE
        elif color == 'pink':
            return colors.PINK
        elif color == 'orange':
            return colors.ORANGE
        elif color == 'red':
            return colors.RED
        elif color == 'yellow':
            return colors.YELLOW
        elif color == 'dark green':
            return colors.DARKGREEN
        elif color == 'blue':
            return colors.BLUE

def text_objects(text, font):
    textSurface = font.render(text, True, colors.BLACK)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None, param1 = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == Monopoly:
                Monopoly()
            elif action == setPnum:
                return setPnum(param1)
            else:
                action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    text = pygame.font.SysFont('comicsansms', 30)
    textSurf, textRect = text_objects(msg, text)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)

def unpause():
    global pause
    pause = False

def paused():
    global pause
    pause = True
    gameDisplay.blit(backgroundImage, ((0, 0)))
    text = pygame.font.SysFont('comicsansms', 115)
    TextSurf, TextRect = text_objects('Paused', text)
    TextRect.center = ((displayWidth/2), (displayHeight/2))
    gameDisplay.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        button('CONTINUE', int(displayWidth/2-(125/640)*displayWidth), int((3/4)*displayHeight), int((12/64)*displayWidth), int((5/48)*displayHeight), colors.GREEN, colors.BRIGHTGREEN, unpause)
        button('MAIN MENU', int((displayWidth/2)+(5/640)*displayWidth), int((3/4)*displayHeight), int((13/64)*displayWidth), int((5/48)*displayHeight), colors.RED, colors.BRIGHTRED, Monopoly)
        pygame.display.update()
        clock.tick(60)

def quitGame():
    pygame.quit()


#============================================================================================


class player():

    def __init__(self, name, icon, num):
        self.name = name
        self.icon = icon
        self.balance = 1500
        self.num = num

    def getName(self):
        return self.name

    def changeName(self, name):
        self.name = name

    def getIcon(self):
        return self.icon

    def changeIcon(self, icon):
        self.icon = icon

    def getBalance(self, dataType):
        if dataType == str:
            return '$' + str(self.balance) + '.00'
        return dataType(self.balance)

    def changeBalance(self, mod):
        self.blance += mod

    def getNum(self):
        return self.num

    def roll(self):
        return(rand.randint(1, 6), rand.randint(1, 6))

def gameIntro():
    gameDisplay.blit(backgroundImage, ((0, 0)))
    largeText = pygame.font.SysFont('comicsansms', 115)
    smallText = pygame.font.SysFont('comicsansms', 30)
    TextSurf, TextRect = text_objects('Monopoly', largeText)
    TextRect.center = (int(displayWidth/2), int(displayHeight/2))
    gameDisplay.blit(TextSurf, TextRect)
    TextSurf, TextRect = text_objects('Ryan J Slater', smallText)
    TextRect.center = ((displayWidth/2), (displayHeight/2)+int((4/48)*displayHeight))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        button('PLAY', int((displayWidth/2)-(165/640)*displayWidth), int((3/4)*displayHeight), int((10/64)*displayWidth), int((5/48)*displayHeight), colors.GREEN, colors.BRIGHTGREEN, gameLoop)
        button('OPTIONS', int((displayWidth/2)-(55/640)*displayWidth), int((3/4)*displayHeight), int((11/64)*displayWidth), int((5/48)*displayHeight), colors.BLUE, colors.BRIGHTBLUE, optionMenu)
        button('QUIT', int((displayWidth/2)+(65/640)*displayWidth), int((3/4)*displayHeight), int((10/64)*displayWidth), int((5/48)*displayHeight), colors.RED, colors.BRIGHTRED, quitGame)

        pygame.display.update()
        clock.tick(60)

def optionMenu():
    # TODO: resource packs like minecraft (board, dice, cards) AND customize each individually in-app
    global displayWidth
    global displayHeight
    gameDisplay.blit(backgroundImage, ((0, 0)))
    text = pygame.font.SysFont('comicsansms', 115)
    TextSurf, TextRect = text_objects('Options', text)
    TextRect.center = ((displayWidth/2), int((5/48)*displayHeight))
    gameDisplay.blit(TextSurf, TextRect)
    buttonWidth = int((11/48)*displayWidth)
    buttonHeight =  int((5/48)*displayHeight)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        button('BACK', int((1/48)*displayWidth), int((1/48)*displayHeight), buttonWidth, buttonHeight, colors.RED, colors.BRIGHTRED, Monopoly)
        pygame.display.update()
        clock.tick(60)

def setPnum(num):
    global pnum
    pnum = num

class space():

    def __init__(self, num, title):
        self.num = num
        self.title = title

    def toString(self):
        return 'Index: ' + str(self.num) + '\nTitle: ' + self.title


class colorProperty(space):
# Standard colored properties
    def __init__(self, num, title, price, mortgage, colorName, color, housePrice, rent, rent1, rent2, rent3, rent4, rentHotel):
        space.__init__(self, num, title)
        self.colorName = colorName
        self.color = color
        self.housePrice = housePrice
        self.rent = rent
        self.rent1 = rent1
        self.rent2 = rent2
        self.rent3 = rent3
        self.rent4 = rent4
        self.rentHotel = rentHotel
        self.mortgage = mortgage
        self.price = price
        self.houses = 0


    def toString(self):
        return(space.toString(self) + '\nColor Name: ' + self.colorName + '\nColor: ' + str(self.color) + '\nPrice: $' + str(self.price) + '\nRent: $' + str(self.rent) + '\n1 House: $' + str(self.rent1) + '\n2 Houses: $' + str(self.rent2) + '\n3 Houses: $' + str(self.rent3) + '\n4 Houses: $' + str(self.rent4) + '\nHotel: $' + str(self.rentHotel) + '\nHouse Price: $' + str(self.housePrice) + '\n# Houses: ' + str(self.houses) + '\nMortgage Value: $' + str(self.mortgage))

    def getNumHouses(self):
        return self.houses

class utility(space):
# Electric Company and Water Works
    def __init__(self, num, title, price=150, mortgage=75, rent=4, rent1=10):
        space.__init__(self, num, title)
        self.price = price
        self.mortgage = mortgage
        self.rent = rent
        self.rent1 = rent1

    def toString(self):
        return(space.toString(self) + '\nPrice: $' + str(self.price) + '\nRent with 1: ' + str(self.rent) + '\nRent with 2: ' + str(self.rent1) + '\nMortgage Value: $' + str(self.mortgage))

class railroad(space):
# Railroads
    def __init__(self, num, title, price, rent1, rent2, rent3, rent4, mortgage):
        space.__init__(self, num, title)
        self.price = price
        self.mortgage = mortgage
        self.rent1 = rent1
        self.rent2 = rent2
        self.rent3 = rent3
        self.rent4 = rent4

    def toString(self):
        return(space.toString(self) + '\nPrice: $' + str(self.price) + '\n1 RR: $' + str(self.rent1) + '\n2 RR: $' + str(self.rent2) + '\n3 RR: $' + str(self.rent3) + '\n4 RR: $' + str(self.rent4) + '\nMortgage Value: $' + str(self.mortgage))

class cardSpace(space):
# Community Chest and Chance spaces
    def __init__(self, num, title):
        space.__init__(self, num, title)
        self.cardType = title

    def toString(self):
        return space.toString(self) + '\nType: ' + self.cardType

class paySpace(space):
# Go, Income Tax (-200), Free Parking (0), Luxury Tax (-75)
    def __init__(self, num, title, pay):
        space.__init__(self, num, title)
        self.pay = pay

    def toString(self):
        return space.toString(self) + '\nPay: $' + str(self.pay)

class jail(space):
# Jail space
    def __init__(self, criminals = []):
        space.__init__(self, 10, 'Jail')
        self.criminals = criminals

    def toString(self):
        string = space.toString(self)
        if len(self.criminals) > 0:
            for i in self.criminals:
                string += i.getName()
        return string

class goToJail(space):
# Go To Jail space
    def __init__(self):
        space.__init__(self, 30, 'Go To Jail')

    def toString(self):
        return space.toString(self)

def getSpaces(pack):
    spaces = []
    file = open(pack + 'spaceData', 'r')
    lines = file.readlines()
    file.close
    spaceStartLines = []
    i = 0
    for line in lines:
        if line[0:5] == 'Index':
            spaceStartLines.append(i)
        i += 1
    index = 0
    for i in spaceStartLines:
        spaceType = lines[i+1]
        title = lines[i+2][7:len(lines[i+2])-1]
        if 'colorProperty' in spaceType:
            spaces.append(colorProperty(index, title, int(lines[i+5][8:]), int(lines[i+14][17:]), lines[i+3][12:len(lines[i+3])-1], colors.getPropertyColor(lines[i+3][12:len(lines[i+3])-1]), int(lines[i+12][14:]), int(lines[i+6][7:]), int(lines[i+7][10:]), int(lines[i+8][11:]), int(lines[i+9][11:]), int(lines[i+10][11:]), int(lines[i+11][8:])))
        elif 'utility' in spaceType:
            spaces.append(utility(index, title, int(lines[i+3][8:]), int(lines[i+6][17:]), int(lines[i+4][13:]), int(lines[i+5][13:])))
        elif 'railroad' in spaceType:
            spaces.append(railroad(index, title, int(lines[i+3][8:]), int(lines[i+4][7:]), int(lines[i+5][7:]), int(lines[i+6][7:]), int(lines[i+7][7:]), int(lines[i+8][17:])))
        elif 'cardSpace' in spaceType:
            spaces.append(cardSpace(index, title))
        elif 'paySpace' in spaceType:
            spaces.append(paySpace(index, title, int(lines[i+3][6:])))
        elif 'jail' in spaceType:
            spaces.append(jail())
        elif 'goToJail' in spaceType:
            spaces.append(goToJail())
        index += 1
    return spaces

def gameLoop():
    global p1, p2, p3, p4
    global pnum
    global displayWidth
    global displayHeight
    global spaces
    global currentPack
    spaces = getSpaces(currentPack)
    die1 = pygame.image.load(currentPack + 'icons/dice/die1.png')
    die2 = pygame.image.load(currentPack + 'icons/dice/die2.png')
    die3 = pygame.image.load(currentPack + 'icons/dice/die3.png')
    die4 = pygame.image.load(currentPack + 'icons/dice/die4.png')
    die5 = pygame.image.load(currentPack + 'icons/dice/die5.png')
    die6 = pygame.image.load(currentPack + 'icons/dice/die6.png')

    pnum = 0
    gameDisplay.blit(backgroundImage, ((0, 0)))
    text = pygame.font.SysFont('comicsansms', 115)
    TextSurf, TextRect = text_objects('How many players?', text)
    TextRect.center = ((displayWidth/2), int((2/5)*displayHeight))
    gameDisplay.blit(TextSurf, TextRect)
    buttonWidth = int((5/48)*displayWidth)
    buttonHeight =  int((5/48)*displayHeight)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        button('2', int((displayWidth-buttonWidth)/2-buttonWidth-10), int((1/2)*displayHeight), buttonWidth, buttonHeight, colors.BLUE, colors.BRIGHTBLUE, setPnum, 2)
        button('3', int((displayWidth-buttonWidth)/2), int((1/2)*displayHeight), buttonWidth, buttonHeight, colors.BLUE, colors.BRIGHTBLUE, setPnum, 3)
        button('4', int((displayWidth-buttonWidth)/2+buttonWidth+10), int((1/2)*displayHeight), buttonWidth, buttonHeight, colors.BLUE, colors.BRIGHTBLUE, setPnum, 4)
        if pnum != 0:
            break
        pygame.display.update()
        clock.tick(60)
    print(str(pnum) + ' players')

    p1 = player('Ryan', currentPack + 'pieces/blueCircle.png', 1)
    roll = p1.roll()
    boardDie1, boardDie2 = die1, die1
    if roll[0] == 1:
        boardDie1 = die1
    elif roll[0] == 2:
        boardDie1 = die2
    elif roll[0] == 3:
        boardDie1 = die3
    elif roll[0] == 4:
        boardDie1 = die4
    elif roll[0] == 5:
        boardDie1 = die5
    elif roll[0] == 6:
        boardDie1 = die6
    if roll[1] == 1:
        boardDie2 = die1
    elif roll[1] == 2:
        boardDie2 = die2
    elif roll[1] == 3:
        boardDie2 = die3
    elif roll[1] == 4:
        boardDie2 = die4
    elif roll[1] == 5:
        boardDie2 = die5
    elif roll[1] == 6:
        boardDie2 = die6

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    paused()
        gameDisplay.blit(backgroundImage, ((0, 0)))
        gameDisplay.blit(boardImage, ((displayWidth-650)/2, (displayHeight-650)/2))
        gameDisplay.blit(boardDie1, ((displayWidth/2-55, 390)))
        gameDisplay.blit(boardDie2, ((displayWidth/2+5, 390)))
        pygame.display.update()
        clock.tick(60)

def Monopoly():
    global displayWidth
    global displayHeight
    global pause
    global gameDisplay
    global clock
    global options
    global boardImage
    global backgroundImage
    global turn
    global currentPack

    pygame.init()
    displayWidth = 1100
    displayHeight = 700
    pause = False
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('Monopoly')
    clock = pygame.time.Clock()
    currentPack = 'resourcePacks/Default/'
    backgroundImage = pygame.image.load(currentPack + 'backgrounds/wood1.png')
    boardImage = pygame.image.load(currentPack + 'board.png')
    turn = 1

    gameIntro()

Monopoly()
