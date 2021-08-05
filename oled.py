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

s = pygame.Surface((128,64), pygame.SRCALPHA, 32)
sWindow = pygame.Surface(windowSize, pygame.SRCALPHA, 32)
screen = pygame.display.set_mode(windowSize)
screen.fill((32,32,32))

def gClear(unused_1):
    global s
    pygame.draw.rect(s, (32,32,32), (0, 0, 128, 64), 0)

def gSetPixel(x, y, c):
    global s
    pygame.draw.line(s, (255,255,255) if c == 1 else (32,32,32), (x, y), (x, y))

def gLine(x1, y1, x2, y2, c):
    global s
    pygame.draw.line(s, (255,255,255) if c == 1 else (32,32,32), (x1, y1), (x2, y2))

def gBox(x1, y1, x2, y2, c):
    global s
    pygame.draw.rect(s, (255,255,255) if c == 1 else (32,32,32), (x1, y1, x2, y2), 1)

def gFillArea(x1, y1, x2, y2, c):
    global s
    pygame.draw.rect(s, (255,255,255) if c == 1 else (32,32,32), (x1, y1, x2, y2), 0)

def gCircle(x, y, size, c):
    global s
    pygame.draw.circle(s, (255,255,255) if c == 1 else (32,32,32), (int(x), int(y)), int(size), 1)

def gFilledCircle(x, y, size, c):
    global s
    pygame.draw.circle(s, (255,255,255) if c == 1 else (32,32,32), (int(x), int(y)), int(size), 0)

def gFlip():
    global s
    global screen

    pygame.transform.scale(s, windowSize, sWindow)

    screen.blit(sWindow, (0, 0))
    pygame.display.flip()

def gInvertArea(x, y, w, h): #/oled/gInvertArea 3 3 $1 121 9
    global s
    global screen

    gFlip()
    inv = pygame.Surface((w, h), pygame.SRCALPHA)
    inv.fill((255,255,255,255))
    inv.blit(s, (- x, -y), None, pygame.BLEND_RGB_SUB)
    s.blit(inv, (x, y), None)
    gFlip()

def gInvertLine(n): #/oled/gInvertLine 0
    if n == 0:
        gInvertArea(0, 8, 128, 9)
    elif n == 1:
        gInvertArea(0, 20, 128, 9)
    elif n == 2:
        gInvertArea(0, 32, 128, 9)
    elif n == 3:
        gInvertArea(0, 44, 128, 9)
    elif n == 4:
        gInvertArea(0, 56, 128, 9)

def gPrintln(x, y, size, c, *txtToPrint):
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

def gCleanln(n):
    if n == 1:
        gFillArea(0, 8, 128, 9, 0)
    elif n == 2:
        gFillArea(0, 20, 128, 9, 0)
    elif n == 3:
        gFillArea(0, 32, 128, 9, 0)
    elif n == 4:
        gFillArea(0, 44, 128, 9, 0)
    elif n == 5:
        gFillArea(0, 56, 128, 9, 0)

def gDrawInfoBar(inL, inR, outL, outR):
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

    gFillArea(0, 0, 128, 8, 0)

    gPrintln(0, 0, 8, 1, "I")
    gPrintln(64, 0, 8, 1, "O")

    for i in range(11):
        gFillArea((i * 5) + 8, 1, 1, 2, 1)
        gFillArea((i * 5) + 8, 5, 1, 2, 1)
    for i in range(inR):
        gFillArea((i * 5) + 7, 0, 3, 4, 1);
    for i in range(inL):
        gFillArea((i * 5) + 7, 4, 3, 4, 1);

    for i in range(11):
        gFillArea((i * 5) + 74, 1, 1, 2, 1)
        gFillArea((i * 5) + 74, 5, 1, 2, 1)
    for i in range(outR):
        gFillArea((i * 5) + 73, 0, 3, 4, 1);
    for i in range(outL):
        gFillArea((i * 5) + 73, 4, 3, 4, 1);

    gFlip()

GDRAW = pygame.event.custom_type()

def gDrawevent(dummy, func, *args):
    pygame.event.post(pygame.event.Event(GDRAW, { 'func': func[0], 'args': args}))

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/gClear", gDrawevent, gClear)
dispatcher.map("/gFlip", gDrawevent, gFlip)
dispatcher.map("/gSetPixel", gDrawevent, gSetPixel)
dispatcher.map("/gLine", gDrawevent, gLine)
dispatcher.map("/gBox", gDrawevent, gBox)
dispatcher.map("/gFillArea", gDrawevent, gFillArea)
dispatcher.map("/gCircle", gDrawevent, gCircle)
dispatcher.map("/gFilledCircle", gDrawevent, gFilledCircle)
dispatcher.map("/gPrintln", gDrawevent, gPrintln)
dispatcher.map("/gCleanln", gDrawevent, gCleanln)
dispatcher.map("/gInvertArea", gDrawevent, gInvertArea)
dispatcher.map("/gInvertLine", gDrawevent, gInvertLine)
dispatcher.map("/gDrawInfoBar", gDrawevent, gDrawInfoBar)


server = osc_server.ThreadingOSCUDPServer(("localhost", 3000), dispatcher)
print("Serving on {}".format(server.server_address))
t = threading.Thread(target=server.serve_forever)
t.daemon = True
t.start()

icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption('Organelle OLED')

while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        server.socket.close() #close server and let close the console
        break
    elif event.type == GDRAW:
        event.func(*event.args)

