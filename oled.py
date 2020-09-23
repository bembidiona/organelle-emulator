import threading
import pygame
import pygame.gfxdraw
import pygame.freetype
from pythonosc import dispatcher
from pythonosc import osc_server
import os.path

SCALERATIO = 2 #size of the pixels. must be an integer

pygame.freetype.init()
fontPath = "assets/organelle.ttf"
print(fontPath)
oFont8 = pygame.freetype.Font(fontPath, 8)
oFont16 = pygame.freetype.Font(fontPath, 16)
oFont24 = pygame.freetype.Font(fontPath, 24)
oFont32 = pygame.freetype.Font(fontPath, 32)
windowSize = (128*SCALERATIO,64*SCALERATIO)

def createOled():
    pygame.display.init() 

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Organelle OLED')

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            server.socket.close() #close server and let close the console
            break


t = threading.Thread(target=createOled)
t.daemon = True
t.start()

s = pygame.Surface((128,64), pygame.SRCALPHA, 32)
sWindow = pygame.Surface(windowSize, pygame.SRCALPHA, 32)
screen = pygame.display.set_mode(windowSize)
screen.fill((32,32,32))

def gClear(unused_addr, unused_1):
    global s
    pygame.draw.rect(s, (32,32,32), (0, 0, 128, 64), 0)

def gSetPixel(unused_addr, x, y, c):
    global s
    pygame.draw.line(s, (255,255,255) if c == 1 else (32,32,32), (x, y), (x, y))

def gLine(unused_addr, x1, y1, x2, y2, c):
    global s
    pygame.draw.line(s, (255,255,255) if c == 1 else (32,32,32), (x1, y1), (x2, y2))

def gBox(unused_addr, x1, y1, x2, y2, c):
    global s
    pygame.draw.rect(s, (255,255,255) if c == 1 else (32,32,32), (x1, y1, x2, y2), 1)

def gFillArea(unused_addr, x1, y1, x2, y2, c):
    global s
    pygame.draw.rect(s, (255,255,255) if c == 1 else (32,32,32), (x1, y1, x2, y2), 0)

def gCircle(unused_addr, x, y, size, c):
    global s
    pygame.draw.circle(s, (255,255,255) if c == 1 else (32,32,32), (int(x), int(y)), int(size), 1)

def gFilledCircle(unused_addr, x, y, size, c):
    global s
    pygame.draw.circle(s, (255,255,255) if c == 1 else (32,32,32), (int(x), int(y)), int(size), 0)

def gFlip(unused_addr):
    global s
    global screen

    pygame.transform.scale(s, windowSize, sWindow)

    screen.blit(sWindow, (0, 0))
    pygame.display.flip()

def gInvertArea(unused_addr, x, y, w, h): #/oled/gInvertArea 3 3 $1 121 9
    global s
    global screen

    gFlip("unused_addr")
    inv = pygame.Surface((w, h), pygame.SRCALPHA)
    inv.fill((255,255,255,255))
    inv.blit(s, (- x, -y), None, pygame.BLEND_RGB_SUB)
    s.blit(inv, (x, y), None)
    gFlip("unused_addr")

def gInvertLine(unused_addr, n): #/oled/gInvertLine 0
    if n == 0:
        gInvertArea("unused_addr", 0, 8, 128, 9)
    elif n == 1:
        gInvertArea("unused_addr", 0, 20, 128, 9)
    elif n == 2:
        gInvertArea("unused_addr", 0, 32, 128, 9)
    elif n == 3:
        gInvertArea("unused_addr", 0, 44, 128, 9)
    elif n == 4:
        gInvertArea("unused_addr", 0, 56, 128, 9)

def gPrintln(unused_addr, x, y, size, c, *txtToPrint):
    global s
    global oFont

    txt = ""

    for word in txtToPrint:
        if type(word) == float:
            word = str(int(word))
        txt = txt + word + " " 

    if size == 8:
        oFont8.render_to(s, (x, y), txt, (255,255,255) if c == 1 else (32,32,32))
    elif size == 16:
        oFont16.render_to(s, (x, y), txt, (255,255,255) if c == 1 else (32,32,32))
    elif size == 24:
        oFont24.render_to(s, (x, y), txt, (255,255,255) if c == 1 else (32,32,32))
    elif size == 32:
        oFont32.render_to(s, (x, y), txt, (255,255,255) if c == 1 else (32,32,32))

def gCleanln(unused_addr, n):
    if n == 1:
        gFillArea("unused_addr", 0, 8, 128, 9, 0)
    elif n == 2:
        gFillArea("unused_addr", 0, 20, 128, 9, 0)
    elif n == 3:
        gFillArea("unused_addr", 0, 32, 128, 9, 0)
    elif n == 4:
        gFillArea("unused_addr", 0, 44, 128, 9, 0)
    elif n == 5:
        gFillArea("unused_addr", 0, 56, 128, 9, 0)

def gDrawInfoBar(unused_addr, inL, inR, outL, outR):
    global s
    global oFont

    inL = int(inL)
    inR = int(inR)
    outL = int(outL)
    outR = int(outR)

    if inR < 0:
        inR = 0
    if inR > 11:
        inR = 11
    if inL < 0:
        inL = 0;
    if inL > 11:
        inL = 11;

    if outR < 0:
        outR = 0
    if outR > 11:
        outR = 11
    if outL < 0:
        outL = 0
    if outL > 11:
        outL = 11

    gFillArea('unused_addr', 0, 0, 128, 8, 0)

    gPrintln("unused_addr", 0, 0, 8, 1, "I")
    gPrintln("unused_addr", 64, 0, 8, 1, "O")

    for i in range(11):
        gFillArea('unused_addr', (i * 5) + 8, 1, 1, 2, 1)
        gFillArea('unused_addr', (i * 5) + 8, 5, 1, 2, 1)
    for i in range(inR):
        gFillArea('unused_addr', (i * 5) + 7, 0, 3, 4, 1);
    for i in range(inL):
        gFillArea('unused_addr', (i * 5) + 7, 4, 3, 4, 1);

    for i in range(11):
        gFillArea('unused_addr', (i * 5) + 74, 1, 1, 2, 1)
        gFillArea('unused_addr', (i * 5) + 74, 5, 1, 2, 1)
    for i in range(outR):
        gFillArea('unused_addr', (i * 5) + 73, 0, 3, 4, 1);
    for i in range(outL):
        gFillArea('unused_addr', (i * 5) + 73, 4, 3, 4, 1);

    gFlip("unused_addr")


dispatcher = dispatcher.Dispatcher()
dispatcher.map("/gClear", gClear)
dispatcher.map("/gFlip", gFlip)
dispatcher.map("/gSetPixel", gSetPixel)
dispatcher.map("/gLine", gLine)
dispatcher.map("/gBox", gBox)
dispatcher.map("/gFillArea", gFillArea)
dispatcher.map("/gCircle", gCircle)
dispatcher.map("/gFilledCircle", gFilledCircle)
dispatcher.map("/gPrintln", gPrintln)
dispatcher.map("/gCleanln", gCleanln)
dispatcher.map("/gInvertArea", gInvertArea)
dispatcher.map("/gInvertLine", gInvertLine)
dispatcher.map("/gDrawInfoBar", gDrawInfoBar)


server = osc_server.ThreadingOSCUDPServer(("localhost", 3000), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()
    
