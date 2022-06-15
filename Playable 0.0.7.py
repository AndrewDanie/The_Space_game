import pygame
import os
import math
from numpy import array, zeros
import copy

pygame.init()
pygame.font.init()

resX = 1000
resY = 580
FPS = 60
dxfr = 100
dyfr = 150
pygame.init()
win = pygame.display.set_mode((resX, resY))
pygame.display.toggle_fullscreen
pygame.display.set_caption('space oddity')
pygame.mouse.set_visible(True)

xwin = 0
ywin = 0

xcam = - resX // 2
ycam = - resY // 2

pygame.mixer.init()
# pygame.mixer.music.load(os.path.join('sounds','Ambient1.mp3'))
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play()
sound1 = pygame.mixer.Sound(os.path.join('sounds', 'engine.wav'))
sound0 = pygame.mixer.Sound(os.path.join('sounds', 'Ambient1.wav'))
############################
sound0.set_volume(0.05)
sound1.set_volume(0.01)

sound0.play(-1)

Frame = pygame.image.load(os.path.join('image', 'Frame.png'))
Frame.convert()
gear = pygame.image.load(os.path.join('image', 'gear.png'))
gear.convert()
gear = pygame.transform.rotozoom(gear, 0, 0.2)

Tank = pygame.image.load(os.path.join('image', 'Tank.png'))
Tank.convert()
Tank = pygame.transform.rotozoom(Tank, 0, 0.2)

L0 = 1
animcount = 0
angle = 0
closeto = 0
xcamq = 0
ycamq = 0

imgdict = {}
Nlevel = 1
changelevel = True
victoryall = False
leveldict = {}
imgdict = {}

datfile = open(os.path.join('data', 'space.init.txt'))

for line in datfile:
    s = line.strip().replace(',', '.').split('\t')

    if s[0] == 'Level':

        if int(s[1]) not in leveldict.keys():
            leveldict[int(s[1])] = False
leveldict[1] = True

anglevictory = 0


class obj():
    def __init__(self, name, x, y, radius, color, mass, vx, vy, freeze, img, zoom, victoryradmin, victoryradmax):
        self.x = x
        self.y = y
        self.vx = float(vx)
        self.vy = float(vy)
        self.axx = float(0)
        self.axy = float(0)
        self.radius = radius
        self.color = color
        self.freeze = freeze
        self.name = name
        self.mass = mass
        self.img = img
        self.img1 = img
        self.victoryradmin = victoryradmin
        self.victoryradmax = victoryradmax
        self.zoom = zoom

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def initialize():
    global ss, ssq
    global victory, victoryall, Live, Fuel, Fuel0, Fuelout
    global victorytime, victorytime0
    global bg, Flame, ship, bodies
    global flamelength, accel
    global datfile
    global Nlevel, changelevel, radmax
    global G, Ktimemin, Ktimemax, ss, ssq
    print(str(Nlevel) + ' init')

    # Fuel = 100000

    bodies = []
    ghostbodies = []

    datfile = open(os.path.join('data', 'space.init.txt'))
    for line in datfile:
        s = line.strip().replace(',', '.').split('\t')
        # s.replace(',', '.')
        # s = line.strip().split('\t')
        if s[0] == 'Level':
            # print('lev')

            if s[1] == str(Nlevel):
                # print(Nlevel)
                G = float(s[3])
                victorytime0 = int(s[4])
                Ktimemin = int(s[5])
                Ktimemax = int(s[6])
                ss = int(s[7])
                radmax = int(s[8])

                if s[1] in imgdict.keys() and not changelevel:
                    bg = imgdict[s[1]]
                else:
                    bg = pygame.image.load(os.path.join('image', s[2]))
                    bg.convert()
                    imgdict[s[1]] = bg
                    print('level.img.' + s[1])

        if s[0] == 'Body':
            if s[1] == str(Nlevel):
                if s[2] in imgdict.keys() and not changelevel:
                    img = imgdict[s[2]]
                else:
                    img0 = pygame.image.load(os.path.join('image', s[13]))
                    img0.convert()
                    img = pygame.transform.rotozoom(img0, 0, float(s[14]))
                    imgdict[s[2]] = img
                    print('body.img.' + s[2])
                bodies.append(
                    obj(s[2], float(s[3]), float(s[4]), int(s[5]), (int(s[6]), int(s[7]), int(s[8])), int(s[9]),
                        float(s[10]), float(s[11]), bool(int(s[12])), img, float(s[14]), int(s[15]), int(s[16])))
                ghostbodies.append(
                    obj(s[2], float(s[3]), float(s[4]), int(s[5]), (int(s[6]), int(s[7]), int(s[8])), int(s[9]),
                        float(s[10]), float(s[11]), bool(int(s[12])), img, float(s[14]), int(s[15]), int(s[16])))

        if s[0] == 'Ship':
            if s[1] == str(Nlevel):
                if s[2] in imgdict.keys() and not changelevel:
                    img = imgdict[s[2]]
                else:
                    img0 = pygame.image.load(os.path.join('image', s[13]))
                    img0.convert()
                    img = pygame.transform.rotozoom(img0, 0, float(s[14]))
                    imgdict[s[2]] = img
                    print('ship.img')

                ship = obj(s[2], float(s[3]), float(s[4]), int(s[5]), (int(s[6]), int(s[7]), int(s[8])), 0,
                           float(s[10]), float(s[11]), bool(int(s[12])), img, float(s[14]), int(s[15]), int(s[16]))
                Fuel0 = int(s[9])
                Fuel = Fuel0
                if 'flame' in imgdict.keys() and not changelevel:
                    Flame = imgdict['flame']
                else:
                    Flame = pygame.image.load(os.path.join('image', s[17]))
                    Flame.convert()
                    Flame = pygame.transform.rotozoom(Flame, 0, float(s[18]))
                    imgdict['flame'] = Flame
                    print('flame.img.' + s[17])
                flamelength = int(s[19])
                accel = float(s[20]) * G

    victorytime = victorytime0
    changelevel = False
    Live = True
    # victoryall = False
    victory = False
    ssq = ss
    for body in bodies:
        body.img1 = pygame.transform.rotozoom(body.img, 0, 1 / ssq)
    print()


# victorytime0 = 10000
# victorytime = victorytime0
imin = 0


def ghostcopy(obj1):  # (self,name,x,y,radius,color,mass,vx,vy,freeze,img,zoom,victoryradmin,victoryradmax):

    obj2 = obj('gh' + obj1.name, obj1.x, obj1.y, obj1.radius, obj1.color, obj1.mass, obj1.vx, obj1.vy, obj1.freeze, 0,
               1, obj1.victoryradmin, obj1.victoryradmax)
    return obj2


def levelup():
    global changelevel, Nlevel
    global leveldict
    global victory, victoryall

    if (Nlevel + 1) in leveldict.keys():
        leveldict[Nlevel + 1] = True
        Nlevel += 1
        print('up')
        changelevel = True
    else:
        print('not up')
        victoryall = True
        # victory = True


framenumber = 0
darrow = 10
anglevictory = 0
rscreen = 100


def drawWindow():
    global angle
    global ssq
    global bodies
    global ssqleft
    global closeto, imin, minxysh
    global dxdymouse
    global pressed
    global XYshWin
    global gear
    global xcamq, ycamq
    global xwin, ywin
    global framenumber
    global anglevictory, rscreen
    global TRAJECTORYX, TRAJECTORYY
    global TRAJECTORYCLOSEX, TRAJECTORYCLOSEY, ghostLive, TCOLL
    global SUNCAM, screensize
    global fuel, victorytime, victorytime0
    # if ktime >1:
    # if animcount % 5*ktime == 0:
    # win.fill((0))
    # else:
    # win.fill((0))

    PLANCAM = True
    SUNCAM = False
    ssqleft = ssq

    minxy = [bodies[imin].x, bodies[imin].y]

    # if minxysh[0] < 250 and minxysh[1] < 150:
    # closeto = 4
    # screensize = 0.5
    if minxysh[0] < 500 - dxfr and minxysh[1] < 300 - dyfr:
        closeto = 3
        screensize = 1
    elif minxysh[0] < 1000 - 2 * dxfr and minxysh[1] < 600 - 2 * dyfr:
        closeto = 2
        screensize = 2
    elif minxysh[0] < 2000 - 4 * dxfr and minxysh[1] < 1200 - 4 * dyfr:
        closeto = 1
        screensize = 4
    elif minxysh[0] < 4000 - 8 * dxfr and minxysh[1] < 2400 - 8 * dyfr:
        closeto = 0
        screensize = 8
    else:
        closeto = 0
        screensize = ss

    framenumber += 1
    if framenumber > 120:
        framenumber = 0

    if keys[pygame.K_e] and not keys[pygame.K_SPACE]:

        ssq = equalizer(ssq, screensize)
        xcamq = equalizer0(xcamq, ship.x / ssq - resX // 2)
        ycamq = equalizer0(ycamq, ship.y / ssq - resY // 2)
        PLANCAM = False
    elif keys[pygame.K_q] or screensize <= 8 and not keys[pygame.K_SPACE] and not bodies[imin].freeze:

        ssq = equalizer(ssq, screensize)
        xcamq = equalizer0(xcamq, int((minxy[0] / ssq) // 1) - resX // 2)
        ycamq = equalizer0(ycamq, int((minxy[1] / ssq) // 1) - resY // 2)

        TRAJECTORYCAMX = equalizer0(xcamq, ((TRAJECTORYCLOSEX / ssq) // 1).astype(int) - resX // 2)
        TRAJECTORYCAMY = equalizer0(ycamq, ((TRAJECTORYCLOSEY / ssq) // 1).astype(int) - resY // 2)
        PLANCAM = True
    elif keys[pygame.K_q] or screensize <= 2 and not keys[pygame.K_SPACE] and bodies[imin].freeze:

        ssq = equalizer(ssq, screensize)
        xcamq = equalizer0(xcamq, int((minxy[0] / ssq) // 1) - resX // 2)
        ycamq = equalizer0(ycamq, int((minxy[1] / ssq) // 1) - resY // 2)
        PLANCAM = False
    elif not keys[pygame.K_SPACE]:

        xcamq = equalizer0(xcamq, xcam)
        ycamq = equalizer0(ycamq, ycam)
        ssq = equalizer(ssq, ss)
        PLANCAM = False
        SUNCAM = True

    else:
        xcamq = equalizer0(xcamq, xcam)
        ycamq = equalizer0(ycamq, ycam)
        ssq = equalizer(ssq, ss)
        PLANCAM = False
        SUNCAM = True

    if ssq != ssqleft:
        for body in bodies:
            body.img1 = pygame.transform.rotozoom(body.img, 0, 1 / ssq)

    win.blit(bg, (0, 0))
    xcamq = int(xcamq // 1)
    ycamq = int(ycamq // 1)

    # ПРЕДСКАЗАТЕЛЬ И РАДАР. ОТРИСОВКА
    # pygame.draw.line(win, (20, 80 + framenumber, 20), [int(ship.x//ssq)-xcamq,int(ship.y//ssq)-ycamq],[int(xwin//ssq)-xcamq,int(ywin//ssq)-ycamq], 3)
    pygame.draw.line(win, (0, min(60 + 3 * framenumber, 255), 60), [
        int(ship.x // ssq) + min(darrow * max(framenumber - 20, 0), rscreen) * math.sin(anglevictory) - xcamq,
        int(ship.y // ssq) + min(darrow * max(framenumber - 20, 0), rscreen) * math.cos(anglevictory) - ycamq],
                     [int(ship.x // ssq) - xcamq + min(darrow * framenumber, rscreen) * math.sin(anglevictory),
                      int(ship.y // ssq) - ycamq + min(darrow * framenumber, rscreen) * math.cos(anglevictory)], 3)

    if PLANCAM and ghostLive:
        for J in range(len(TRAJECTORYX)):
            if J % 10 == 0 and ssq == ssqleft:
                br = int((255 - 240 / len(TRAJECTORYX) * J) // 1)
                pygame.draw.circle(win, (br, br, br), (int((TRAJECTORYX[J] // ssq - TRAJECTORYCAMX[J]) // 1),
                                                       int((TRAJECTORYY[J] // ssq - TRAJECTORYCAMY[J]) // 1)), 2)

    elif PLANCAM:
        for J in range(TCOLL):
            if J % 10 == 0 and ssq == ssqleft:
                br = int((255 - 240 / len(TRAJECTORYX) * J) // 1)
                pygame.draw.circle(win, (br, br, br), (int((TRAJECTORYX[J] // ssq - TRAJECTORYCAMX[J]) // 1),
                                                       int((TRAJECTORYY[J] // ssq - TRAJECTORYCAMY[J]) // 1)), 2)
                pygame.draw.circle(win, (255, 0, 0), (int((TRAJECTORYX[TCOLL] // ssq - TRAJECTORYCAMX[TCOLL]) // 1),
                                                      int((TRAJECTORYY[TCOLL] // ssq - TRAJECTORYCAMY[TCOLL]) // 1)),
                                   10)

    if SUNCAM and ghostLive:
        for J in range(len(TRAJECTORYX)):
            if J % 10 == 0 and ssq == ssqleft:
                br = int((255 - 240 / len(TRAJECTORYX) * J) // 1)
                pygame.draw.circle(win, (br, br, br), (
                int((TRAJECTORYX[J] // ssq - xcamq) // 1), int((TRAJECTORYY[J] // ssq - ycamq) // 1)), 2)

    elif SUNCAM:
        for J in range(TCOLL):
            if J % 10 == 0 and ssq == ssqleft:
                br = int((255 - 240 / len(TRAJECTORYX) * J) // 1)
                pygame.draw.circle(win, (br, br, br), (
                int((TRAJECTORYX[J] // ssq - xcamq) // 1), int((TRAJECTORYY[J] // ssq - ycamq) // 1)), 2)
                pygame.draw.circle(win, (255, 0, 0), (
                int((TRAJECTORYX[TCOLL] // ssq - xcamq) // 1), int((TRAJECTORYY[TCOLL] // ssq - ycamq) // 1)), 5)

    # ПЛАНЕТЫ

    for i in range(len(bodies)):
        if bodies[i].img != []:
            rect = bodies[i].img1.get_rect()
            rect.center = (int(bodies[i].x // ssq) - xcamq, int(bodies[i].y // ssq) - ycamq)
            # pygame.draw.rect(bodies[i].img1, (55,55,55), rect, 10)
            win.blit(bodies[i].img1, rect)
        if bodies[i].victoryradmax > 0:
            pygame.draw.circle(win, (0, 255, 0), (int(bodies[i].x // ssq) - xcamq, int(bodies[i].y // ssq) - ycamq),
                               max(int(bodies[i].victoryradmax / ssq // 1), 12), 1)
            xwin = bodies[i].x
            ywin = bodies[i].y
            rscreen = math.sqrt(((xwin - ship.x) // ssq) ** 2 + ((ywin - ship.y) // ssq) ** 2)
            anglevictory = (math.atan2(int(xwin - ship.x), int(ywin - ship.y)))
            # pygame.draw.line(win, (255, 255, 255), [int(ship.x//ssq)-xcamq,int(ship.y//ssq)-ycamq],[int(bodies[i].x//ssq)-xcamq,int(bodies[i].y//ssq)-ycamq], 3)
        if bodies[i].victoryradmin > 0:
            pygame.draw.circle(win, (0, 255, 0), (int(bodies[i].x // ssq) - xcamq, int(bodies[i].y // ssq) - ycamq),
                               max(int(bodies[i].victoryradmin / ssq // 1), 8), 1)

        pygame.draw.circle(win, bodies[i].color, (int(bodies[i].x // ssq) - xcamq, int(bodies[i].y // ssq) - ycamq),
                           max(int((bodies[i].radius / ssq) // 1), 5), 1)
    # pygame.draw.circle(win,ship.color,(int(ship.x//ssq)-xcamq,int(ship.y//ssq)-ycamq),ship.radius//ssq)

    SHIP = pygame.transform.rotozoom(ship.img, 180 - angle, 1)
    rectsh = SHIP.get_rect()
    XYshWin = [int(ship.x // ssq) - xcamq, int(ship.y // ssq) - ycamq]
    rectsh.center = (XYshWin[0], XYshWin[1])
    win.blit(SHIP, rectsh)

    angle = int(57.3 * math.atan2(dxdymouse[1], dxdymouse[0]) // 1)

    if ax:
        axx = int(((accelx / accel) * flamelength // 1))
        axy = int(((accely / accel) * flamelength // 1))

        if not pressed[0]:
            angle = int(57.3 * math.atan2(axy, axx) // 1)
        img = pygame.transform.rotozoom(Flame, 180 - angle, 1)
        rect1 = img.get_rect()
        rect1.center = (int(ship.x // ssq) - xcamq - axx * (3), int(ship.y // ssq) - ycamq - axy * (3))
        win.blit(img, rect1)
        # for i in range(4):
        # pygame.draw.circle(win,(0,55,255),(int(ship.x//ssq)-xcamq - axx*(i+1) ,int(ship.y//ssq)-ycamq-axy*(i+1)),4-i)
    # if abs(XYshWin[0]) > 0.7*resX:
    # sscurrent += 0

    # РАМКА И GUI

    win.blit(Frame, (0, 0))  # РАМКА
    f1 = pygame.font.SysFont('Arial', 30)
    string2 = 'arrows - acceleration. lshift - timewarp q/e - planetary/ship camera. f - restart'
    # text1 = f1.render(string, 1, (180, 50, 50))
    text2 = f1.render(string2, 1, (255, 255, 255))
    # win.blit(text1, (50 , 1))
    win.blit(text2, (50, 500))
    pygame.draw.rect(win, (255, 255, 255), (pos[0] - 5, pos[1] - 5, 10, 10), 2)

    gear1 = pygame.transform.rotozoom(gear, int((360 * animcount / FPS) // 1), 1)
    rectgear = gear1.get_rect()
    rectgear.center = (1000, 580)
    win.blit(gear1, rectgear)

    win.blit(Tank, (0, 379))
    persentageFuel = ((Fuel * 100 / Fuel0))
    BarShift = int((1 - Fuel / Fuel0) * 180)
    pygame.draw.rect(win, (255, max(0, 255 * (Fuel / Fuel0)), max(0, 255 * (Fuel / Fuel0))),
                     (9, 388 + BarShift, 22, 180 - BarShift))

    pygame.draw.rect(win, (50, 50, 50), (5, 5, 990, 26))
    pygame.draw.rect(win, (100 + 50 * (1 - victorytime / victorytime0), 50 + 200 * (1 - victorytime / victorytime0),
                           50 + 100 * (1 - victorytime / victorytime0)),
                     (6, 8, 988 * (1 - (victorytime / victorytime0)), 20))

    pygame.display.update()


def equalizer(a, b=False):
    if b == False:
        return (a)(victorytime / victorytime0)
    elif abs((a - b) / b) < 0.1:
        return (b)
    else:
        return (a + (b - a) / 5)


def equalizer0(a, b):
    return (b)


def gravity():
    global Live, victory, Fuel, ax
    global KT1, radmax
    global closeto
    global XYshWin, minxysh
    # global minxy
    global imin
    global victorytime

    rshmin = 100000
    # radmin = 0
    # closeto = 0
    mbodyclosest = 1

    # imin = 0
    for t in range(ktime):
        ship.axx = 0.0
        ship.axy = 0.0
        if ax:
            Fuel -= 1
        for i in range(len(bodies)):

            if bodies[i].mass >= 0:
                dxsh = (ship.x - bodies[i].x) * L0
                dysh = (ship.y - bodies[i].y) * L0
                rsh = math.sqrt(dxsh * dxsh + dysh * dysh)

                if rsh < rshmin:
                    rshmin = rsh
                    imin = i
                    mbodyclosest = bodies[i].mass
                    minxysh = [abs(dxsh), abs(dysh)]
                ship.axx -= bodies[i].mass * G * dxsh / rsh ** 3
                ship.axy -= bodies[i].mass * G * dysh / rsh ** 3

                if rsh < bodies[i].radius or rshmin > radmax:
                    Live = False
                if bodies[i].victoryradmax > 0:
                    if rsh <= bodies[i].victoryradmax and rsh > bodies[i].victoryradmin:
                        victorytime -= 1
                    else:

                        victorytime = victorytime0
                if victorytime <= 0:
                    victory = True
                if Fuel < 1 and victorytime == victorytime0:
                    Live = False
                    Fuelout = True

        ship.x += ship.vx + accelx / 2
        ship.y += ship.vy + accely / 2

        ship.vx += (ship.axx + accelx)
        ship.vy += (ship.axy + accely)

        for body1 in bodies:
            body1.axx = 0.0
            body1.axy = 0.0
            for body2 in bodies:
                if body1 != body2 and not body1.freeze and body2.mass > 0:
                    dx = (body1.x - body2.x) * L0
                    dy = (body1.y - body2.y) * L0
                    r = (dx ** 2 + dy ** 2) ** 0.5
                    body1.axx -= body2.mass * G * dx / r ** 3
                    body1.axy -= body2.mass * G * dy / r ** 3
                    if r < (body1.radius + body2.radius):
                        if body2.mass > body1.mass:
                            bodies.pop(bodies.index(body1))
                        elif body2.mass < body1.mass:
                            bodies.pop(bodies.index(body2))
                        else:
                            bodies.pop(bodies.index(body1))
                            bodies.pop(bodies.index(body2))

            body1.x += body1.vx + body1.axx / 2
            body1.y += body1.vy + body1.axy / 2
            body1.vx += body1.axx
            body1.vy += body1.axy


SUNCAM = False
screensize = 1
TCOLL = 10


def prognose(ship, bodies):
    global ghostbodies
    global ghostLive, TRAJECTORYX, TRAJECTORYY, TCOLL
    global TRAJECTORYCLOSEX, TRAJECTORYCLOSEY
    global xcamq, ycamq, imin, ktime
    global ssq, SUNCAM, screensize

    # TimeAmplShift = int(( ktime / Ktimemin) // 1)
    TimeAmplifyer = 2 * screensize

    TimeAmp1 = 50
    # ghostship = copy.copy(ship)
    # ghostbodies = copy.copy(bodies)

    ghostship = ghostcopy(ship)
    ghostbodies = []
    for i in range(len(bodies)):
        ghostbodies += [ghostcopy(bodies[i])]

    rshmin = 100000
    ghostLive = True

    TRAJECTORYX = zeros(Ktimemin * TimeAmp1)
    TRAJECTORYY = zeros(Ktimemin * TimeAmp1)
    TRAJECTORYCLOSEX = zeros(Ktimemin * TimeAmp1)
    TRAJECTORYCLOSEY = zeros(Ktimemin * TimeAmp1)

    for t in range(Ktimemin * TimeAmp1):
        ghostship.axx = 0.0
        ghostship.axy = 0.0
        for i in range(len(bodies)):

            if bodies[i].mass >= 0:
                dxghostship = (ghostship.x - ghostbodies[i].x) * L0
                dyghostship = (ghostship.y - ghostbodies[i].y) * L0
                ghostshipradius = math.sqrt(dxghostship ** 2 + dyghostship ** 2)

                if ghostshipradius < rshmin:
                    rshmin = ghostshipradius
                ghostship.axx -= ghostbodies[i].mass * G * dxghostship / ghostshipradius ** 3
                ghostship.axy -= ghostbodies[i].mass * G * dyghostship / ghostshipradius ** 3

            if ghostshipradius < ghostbodies[i].radius and ghostLive:
                ghostLive = False
                TCOLL = t
                break

        ghostship.x += ghostship.vx * TimeAmplifyer + ghostship.axx * TimeAmplifyer ** 2 / 2
        ghostship.y += ghostship.vy * TimeAmplifyer + ghostship.axy * TimeAmplifyer ** 2 / 2

        TRAJECTORYX[t] = ghostship.x
        TRAJECTORYY[t] = ghostship.y

        ghostship.vx += (ghostship.axx) * TimeAmplifyer
        ghostship.vy += (ghostship.axy) * TimeAmplifyer

        for i in range(len(ghostbodies)):
            ghostbodies[i].axx = 0.0
            ghostbodies[i].axy = 0.0
            for j in range(len(ghostbodies)):
                if i != j and not ghostbodies[i].freeze and ghostbodies[j].mass > 0:
                    dxgh = (ghostbodies[i].x - ghostbodies[j].x) * L0
                    dygh = (ghostbodies[i].y - ghostbodies[j].y) * L0
                    rgh = (dxgh ** 2 + dygh ** 2) ** 0.5
                    ghostbodies[i].axx -= ghostbodies[j].mass * G * dxgh / rgh ** 3
                    ghostbodies[i].axy -= ghostbodies[j].mass * G * dygh / rgh ** 3

            ghostbodies[i].x += ghostbodies[i].vx * TimeAmplifyer + ghostbodies[i].axx * TimeAmplifyer ** 2 / 2
            ghostbodies[i].y += ghostbodies[i].vy * TimeAmplifyer + ghostbodies[i].axy * TimeAmplifyer ** 2 / 2
            ghostbodies[i].vx += ghostbodies[i].axx * TimeAmplifyer
            ghostbodies[i].vy += ghostbodies[i].axy * TimeAmplifyer

        TRAJECTORYCLOSEX[t] = ghostbodies[imin].x
        TRAJECTORYCLOSEY[t] = ghostbodies[imin].y


# ------------------------------------------------------------------------------------

# if keys[pygame.K_e] and not keys[pygame.K_SPACE]:

#     ssq = equalizer(ssq,screensize)
#     TRAJECTORYCAMX = equalizer0(xcamq,ship.x / ssq- resX // 2)
#     TRAJECTORYCAMX = equalizer0(ycamq,ship.y / ssq - resY // 2)

# elif keys[pygame.K_q] or screensize <= 8 and not keys[pygame.K_SPACE] and not bodies[imin].freeze:

#     ssq = equalizer(ssq,screensize)
#     xcamq = equalizer0(xcamq,int((minxy[0] / ssq) // 1) - resX // 2)
#     ycamq = equalizer0(ycamq,int((minxy[1] / ssq) // 1)  - resY // 2)

# elif keys[pygame.K_q] or screensize <= 2 and not keys[pygame.K_SPACE] and bodies[imin].freeze:

#     ssq = equalizer(ssq,screensize)
#     xcamq = equalizer0(xcamq,int((minxy[0] / ssq) // 1) - resX // 2)
#     ycamq = equalizer0(ycamq,int((minxy[1] / ssq) // 1)  - resY // 2)


#         TRAJECTORYCAMX


# -------------------------------------------------------------------------------------
def mouse():
    global XYshWin
    global ssq
    global dxdymouse
    global pressed
    global pos

    dxdymouse = [pos[0] - XYshWin[0], pos[1] - XYshWin[1]]


def keyboard():
    global run, Live
    global angle
    global keyaccel
    global ktime, TimeAmplShift
    global KT1
    global keys
    global pressed
    global pos
    global ax
    global accelx, accely
    global Live, victory
    global Nlevel, changelevel
    keyaccel = False
    keys = pygame.key.get_pressed()
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()

    ax = False
    accelx = 0
    accely = 0
    # for i in pygame.event.get():
    #     if i.type == pygame.QUIT:
    #         exit()
    #     elif i.type == pygame.KEYDOWN:
    #         if i.key == pygame.K_f:
    #             initialize()
    #         if i.key == pygame.K_1:
    #             Nlevel = 1
    #             initialize()
    #         if i.key == pygame.K_2:
    #             Nlevel = 2
    #             initialize()
    #         if i.key == pygame.K_3:
    #             Nlevel = 3
    #             initialize()
    #         if i.key == pygame.K_k:
    #             Live = False
    #         if i.key == pygame.K_v:
    #             victory == True
    #             print('forcevic')
    #             #Live = False

    if keys[pygame.K_ESCAPE]:
        run = False
    elif keys[pygame.K_LCTRL]:
        ktime = 1 * KT1
    elif keys[pygame.K_LSHIFT]:
        ktime = Ktimemax * KT1
    else:
        ktime = Ktimemin * KT1

    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
            keyaccel = False
        elif keys[pygame.K_UP]:
            keyaccel = True
            angle = -90
        elif keys[pygame.K_DOWN]:
            keyaccel = True
            angle = 90
    elif keys[pygame.K_UP] and keys[pygame.K_DOWN]:
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            keyaccel = False
        elif keys[pygame.K_LEFT]:
            keyaccel = True
            angle = 180
        elif keys[pygame.K_RIGHT]:
            keyaccel = True
            angle = 0




    elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        keyaccel = True
        angle = -135
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        keyaccel = True
        angle = 135
    elif keys[pygame.K_LEFT]:
        keyaccel = True
        angle = 180
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        keyaccel = True
        angle = -45
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        keyaccel = True
        angle = 45
    elif keys[pygame.K_RIGHT]:
        keyaccel = True
        angle = 0
    elif keys[pygame.K_UP]:
        keyaccel = True
        angle = -90
    elif keys[pygame.K_DOWN]:
        keyaccel = True
        angle = 90


# Year - 180000 ticks

run = True
clock = pygame.time.Clock()
ktime = 1
KT1 = 1
Live = True
XYshWin = [0, 0]
pos = [0, 0]
initialize()
prognose(ship, bodies)
ssq = ss

TimeAmplifyer = 50
TimeAmplShift = int((Ktimemax / Ktimemin) // 1)
TimeAmp1 = 10
TRAJECTORYX = zeros(Ktimemin * TimeAmp1)
TRAJECTORYY = zeros(Ktimemin * TimeAmp1)
TRAJECTORYCLOSEX = zeros(Ktimemin * TimeAmp1)
TRAJECTORYCLOSEY = zeros(Ktimemin * TimeAmp1)

while (run):
    if (Live) and not victory and not victoryall:
        clock.tick(FPS)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False

            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_f:
                    initialize()
                if i.key == pygame.K_1:
                    Nlevel = 1
                    changelevel = True
                    initialize()
                if i.key == pygame.K_2:
                    Nlevel = 2
                    changelevel = True
                    initialize()
                if i.key == pygame.K_3:
                    Nlevel = 3
                    changelevel = True
                    initialize()
                if i.key == pygame.K_4:
                    Nlevel = 4
                    changelevel = True
                    initialize()
                if i.key == pygame.K_5:
                    Nlevel = 5
                    changelevel = True
                    initialize()
                if i.key == pygame.K_k:
                    Live = False
                    print('forcedeath')
                if i.key == pygame.K_v:
                    victory = True
                    print('forcevic')

        if animcount + 1 >= FPS:
            animcount = 0
        else:
            animcount += 1

        keyboard()
        mouse()
        string = 'x= ' + str((dxdymouse[0]) // 0.1) + ' y= ' + str((dxdymouse[1]) // 0.1) + '   KTIME = ' + str(
            ktime) + '   Level = ' + str(Nlevel) + '    victorytime' + str(victorytime) + '  Fuel = ' + str(
            int(((Fuel / Fuel0 * 100) // 1))) + '%'
        # string = 'x= '+ str((xwin)//0.1) + ' y= ' + str((ywin)//0.1) + '   victoryangle = ' + str( anglevictory) + '   rscreen = '+ str(rscreen) + '    victorytime' + str(victorytime) + '  Fuel = ' + str(int(((Fuel / Fuel0 * 100 ) // 1))) + '%'
        if (pressed[0] or keyaccel) and Fuel >= 0:
            accelx = accel * math.cos(math.radians(angle))
            accely = accel * math.sin(math.radians(angle))
        if accelx != 0 or accely != 0:
            ax = True

        if Live and not victory:

            gravity()
            drawWindow()
            if ax:
                sound1.play()
            if (animcount % 10 == 0 and not ax) or (ax and animcount % 2 == 0):
                prognose(ship, bodies)

    if not (Live) or victory or victoryall:
        clock.tick(30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_f) or (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if victoryall:
                    Nlevel = 1
                    print('vic2 ' + str(Nlevel))
                    print(str(victory) + str(victoryall))
                    changelevel = True

                    victoryall = False
                elif victory:
                    levelup()
                    print('vic')

                else:
                    print('dead')

                initialize()
                continue

        if not victory and not victoryall:
            f1 = pygame.font.SysFont('Arial', 150)
            text1 = f1.render('YOU DIED', 1, (180, 0, 0))
            f2 = pygame.font.SysFont('Arial', 50)
            text2 = f2.render('press f to pay respect', 1, (180, 0, 0))
            win.fill((0))
            win.blit(text1, (200, 150))
            win.blit(text2, (300, 300))
        elif victoryall:
            f1 = pygame.font.SysFont('Arial', 150)
            text1 = f1.render('Victory', 1, (100, 255, 100))

            f2 = pygame.font.SysFont('Arial', 50)
            text2 = f2.render('Congratulations', 1, (100, 255, 100))
            win.fill((0))
            win.blit(text1, (300, 180))
            win.blit(text2, (300, 400))
        else:
            f1 = pygame.font.SysFont('Arial', 150)
            text1 = f1.render('Victory', 1, (100, 255, 100))

            f2 = pygame.font.SysFont('Arial', 50)
            text2 = f2.render('press f to play next', 1, (100, 255, 100))
            win.fill((0))
            win.blit(text1, (300, 180))
            win.blit(text2, (300, 400))

        pygame.display.update()
pygame.mixer.quit()
datfile.close()
pygame.quit()  # 317 - 235 = 82