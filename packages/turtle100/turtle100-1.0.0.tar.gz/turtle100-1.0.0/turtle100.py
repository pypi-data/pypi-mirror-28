import turtle
import random
def drawShape(sides, length):
    angle = 360.0 / sides
    for i in range(sides):
        turtle.forward(length)
        turtle.right(angle)
def moveTurtle(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
def drawTriangle(length):
    drawShape(3, length)
def drawSquare(length):
    drawShape(4, length)
def drawCircle(length):
    drawShape(360, length)
def drawRandom():
    x = random.randrange(-200,200)
    y = random.randrange(-200,200)
    length = random.randint(1,101)
    shape = random.randint(1,4)
    moveTurtle(x, y)
    if shape == 1:
        drawTriangle(length)
    elif shape == 2:
        drawSquare(length)
    elif shape == 3:
        length = length % 4
        drawCircle(length)
for j in range(1,100):
    drawRandom()
turtle.done()