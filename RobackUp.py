"""
  Nombre:   David Osollo
  Proyecto: Proyecto Robotina
  Materia:  Computacón Cognitiva
"""


import tkinter # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from PIL import ImageTk,Image
import numpy as np
import random
import time
from random import randint, uniform, random

"""
  Declaracion de variables globales
"""
init_color = '#9FBEBC'
init_outline_color = '#365566'
init_new_color = '#E3B697'
lienzo_principal = None
imgRobotina = None
photoRobotina = None
imgCuadroAzul = None
photoCuadroAzul = None
imgCuadroAmarillo = None
photoCuadroAmarillo = None
imgToilet = None
photoToilet = None
imgBasura = None
photoBasura = None
imgCama = None
photoCama = None
imgCocinar = None
photoCocinar = None
imgPila = None
photoPila = None
imgPlanchar = None
photoPlanchar = None
image_to_show = None
arr_tareas = None
imgCocinaHerr = None
photoCocinaHerr = None
imgEscoba = None
photoEscoba = None
imgLimpBano = None
photoLimpBano = None
RoboCasilla = None
imgLimpio = None
photoLimpio = None
RoboMoveTime = 0.15
RoboMoveLimpiaTime = 1.5

casillas_tareas_map = {}
casillas_logistica_map = {}

arr_tareas = np.array([])
RoboTrayectoria = np.array([])

frame_size = 50
offset_y = 0
offset_x = 70
numRens = 10
numCols = 20

mainWin = tkinter.Tk()
mainWin.title("Proyecto Robotina")

#mainWin.geometry("1000x700")

class casilla_frame(object):
    def __init__(self, canvas, tipo_casilla, col, ren,size, offset_y, offset_x, color, img):
        self.canvas = canvas
        self.col = col
        self.ren = ren
        self.size = size
        self.offset_y = offset_y
        self.offset_x = offset_x
        self.color = color
        self.img = img
        self.tipo_casilla = tipo_casilla
        self.id = self.canvas.create_image((col-1) * size + offset_x, ren * size + offset_y, image=img, anchor="nw")

    def Touch(self, col,ren,iEje):

        global casillas_tareas_map
        global numRens
        global numCols
        x = None
        y = None
        tarea = None

        # Checar si esta ocupado
        for tarea in casillas_tareas_map:
            x, y = casillas_tareas_map[tarea].GetCoord()

            if iEje == 0:
                if ((x == self.col + 1 or x == self.col - 1) and y == ren) or ((y == self.ren + 1 or y == self.ren - 1) and x == col):
                    return 1
            if iEje == 1:
                if (x == self.col + 1 or x == self.col - 1) and (y == self.ren):
                    return 1
            elif iEje == 2:
                if (y == self.ren + 1 or y == self.ren - 1) and (x == self.col):
                    return 1
        return 0

    def Move(self, col, ren, colGol, renGol):

        global casillas_tareas_map
        global numRens
        global numCols
        x = None
        y = None
        tarea = None

        #Checar si esta ocupado
        for tarea in casillas_tareas_map:
            x, y = casillas_tareas_map[tarea].GetCoord()
            if (colGol == self.col + col) and (renGol == self.ren + ren):
                break

            if x == self.col + col and y == self.ren + ren:
                return 1

            if 0 > (self.col + col) or 0 > (self.ren + ren) or numCols <= (self.col + col) or numRens <= (self.ren + ren):
                return 2


        self.col = self.col + col
        self.ren = self.ren + ren

        self.canvas.move(self.id, col * self.size , ren * self.size )
        self.canvas.tag_raise(self.id)

        return 0

    def GetCoord(self):
        return (self.col, self.ren)

    def Limpiar(self, imgClean):
        self.canvas.itemconfig(self.id, image=imgClean)

def init_app():
    global lienzo_principal
    global imgRobotina
    global photoRobotina
    global imgCuadroAzul
    global photoCuadroAzul
    global imgCuadroAmarillo
    global photoCuadroAmarillo
    global imgToilet
    global photoToilet
    global imgBasura
    global photoBasura
    global imgCama
    global photoCama
    global imgCocinar
    global photoCocinar
    global imgPila
    global photoPila
    global imgPlanchar
    global photoPlanchar
    global image_to_show
    global imgCocinaHerr
    global photoCocinaHerr
    global imgEscoba
    global photoEscoba
    global imgLimpBano
    global photoLimpBano
    global imgLimpio
    global photoLimpio

    lienzo_principal = tkinter.Canvas(mainWin, borderwidth=1, width=frame_size * numCols + offset_x,
                            height=frame_size * numRens + offset_y)

    imgRobotina = Image.open("./img/Robotina.png").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoRobotina = ImageTk.PhotoImage(imgRobotina)

    #Imagenes Tareas
    imgCuadroAzul = Image.open("./img/square_blue.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoCuadroAzul = ImageTk.PhotoImage(imgCuadroAzul)

    imgCuadroAmarillo = Image.open("./img/square_yellow.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoCuadroAmarillo = ImageTk.PhotoImage(imgCuadroAmarillo)

    imgToilet = Image.open("./img/toilet.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoToilet = ImageTk.PhotoImage(imgToilet)

    imgBasura = Image.open("./img/basura.jpeg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoBasura = ImageTk.PhotoImage(imgBasura)

    imgCocinar = Image.open("./img/cocinar.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoCocinar = ImageTk.PhotoImage(imgCocinar)

    imgPlanchar = Image.open("./img/planchar.png").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoPlanchar = ImageTk.PhotoImage(imgPlanchar)

    #Imagenes Recargar
    imgCama = Image.open("./img/cama.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoCama = ImageTk.PhotoImage(imgCama)

    imgPila = Image.open("./img/pila.png").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoPila = ImageTk.PhotoImage(imgPila)

    #Imagenes Herramientas

    imgPlancha = Image.open("./img/plancha.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoPlancha = ImageTk.PhotoImage(imgPlancha)

    imgCocinaHerr = Image.open("./img/cocina_herr.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoCocinaHerr = ImageTk.PhotoImage(imgCocinaHerr)

    imgEscoba = Image.open("./img/escoba.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoEscoba = ImageTk.PhotoImage(imgEscoba)

    imgLimpBano = Image.open("./img/limpiabanos.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoLimpBano = ImageTk.PhotoImage(imgLimpBano)

    imgLimpio = Image.open("./img/limpio.jpeg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoLimpio = ImageTk.PhotoImage(imgLimpio)

def set_tasks():
    global lienzo_principal
    global imgRobotina
    global photoRobotina
    global imgCuadroAzul
    global photoCuadroAzul
    global imgToilet
    global photoToilet
    global imgBasura
    global photoBasura
    global imgCama
    global photoCama
    global imgCocinar
    global photoCocinar
    global imgPila
    global photoPila
    global imgPlanchar
    global photoPlanchar
    global image_to_show
    global arr_tareas
    global imgCocinaHerr
    global photoCocinaHerr
    global imgEscoba
    global photoEscoba
    global imgLimpBano
    global photoLimpBano
    global RoboCasilla
    global arr_tareas
    global RoboTrayectoria

    casillas_tareas_map.clear()
    casillas_logistica_map.clear()

    Tipo_Casilla = None
    arr_tareas = None
    RoboTrayectoria = None

    for col in range(numCols):
        for ren in range(numRens):
            if col == 2 and ren == 0:
                image_to_show = photoPila
                Tipo_Casilla = 1
            elif col == 4 and ren == 0:
                image_to_show = photoCama
                Tipo_Casilla = 2
            elif col == 6 and ren == 0:
                image_to_show = photoCocinaHerr
                Tipo_Casilla = 3
            elif col == 8 and ren == 0:
                image_to_show = photoEscoba
                Tipo_Casilla = 4
            elif col == 10 and ren == 0:
                image_to_show = photoLimpBano
                Tipo_Casilla = 5
            else:
                tarea = random.randint(1, 35)
                if ren == 0 or ren == 1:
                    image_to_show = photoCuadroAmarillo
                    Tipo_Casilla = 0

                if ren != 0 and ren != 1:
                    if tarea == 1 and np.count_nonzero(arr_tareas == tarea) < 2:
                        image_to_show = photoPlanchar
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 6
                    elif tarea == 2 and np.count_nonzero(arr_tareas == tarea) < 2:
                        image_to_show = photoCocinar
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 7
                    elif tarea == 3 and np.count_nonzero(arr_tareas == tarea) < 2:
                        image_to_show = photoBasura
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 8
                    elif tarea == 4 and np.count_nonzero(arr_tareas == tarea) < 2:
                        image_to_show = photoToilet
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 9
                    else:
                        image_to_show = photoCuadroAzul
                        Tipo_Casilla = 0

            casilla = casilla_frame(lienzo_principal, Tipo_Casilla, col, ren, frame_size, offset_y, offset_x, init_color,
                                    image_to_show)

            if (Tipo_Casilla >= 1) and (Tipo_Casilla <=5):
                casillas_logistica_map[casilla.id] = casilla
            elif (Tipo_Casilla >= 6) and (Tipo_Casilla <=9):
                casillas_tareas_map[casilla.id] = casilla

    image_to_show = photoRobotina
    RoboCasilla = casilla_frame(lienzo_principal, 10, 0, 0, frame_size, offset_y, offset_x, init_color, image_to_show)

def funcion():
	print('Exelente')

def LimpiarBtn():
    RoboLimpia()

def RoboLimpia():
    # Checar si esta ocupado
    for tarea in casillas_tareas_map:
        x, y = casillas_tareas_map[tarea].GetCoord()
        goRobot(x, y)
        time.sleep(RoboMoveLimpiaTime)
        casillas_tareas_map[tarea].Limpiar(photoLimpio)
        lienzo_principal.update()

    goRobot(1, 1)
    goRobot(0, 0)



def Unstuck(xM, yM, x2, y2):

    iDirectinY = -1
    iDirectinX = 1

    iDirectinXOri = 1
    iDirectinYOri = 1

    x = 0
    y = 0
    xIni = 0
    yIni = 0

    bStuck = True
    iReturnMove = 0

    x, y = RoboCasilla.GetCoord()
    xIni = x
    yIni = y

    if y <= y2:
        iDirectinY = 1
        iDirectinYOri = 1
    else:
        iDirectinY = -1
        iDirectinYOri = -1
        #else:
    if x <= x2:
        iDirectinX = 1
        iDirectinXOri = 1
    else:
        iDirectinX = -1
        iDirectinXOri = -1

    while bStuck == True:

        if iDirectinX == 1:
            iReturnMove = RoboCasilla.Move(1, 0, x2, y2)
            if iReturnMove == 0:
                time.sleep(RoboMoveTime)
                x, y = RoboCasilla.GetCoord()
                lienzo_principal.update()
                iDirectinY = iDirectinYOri
            else:
                iDirectinX = -iDirectinX

        else:
            iReturnMove = RoboCasilla.Move(-1, 0, x2, y2)
            if iReturnMove == 0:
                time.sleep(RoboMoveTime)
                x, y = RoboCasilla.GetCoord()
                lienzo_principal.update()
                iDirectinY = iDirectinYOri
            else:
                iDirectinX = -iDirectinX


        if xM != 0:
            if xM == 1 and (x - xIni) >= 1:
                bStuck = False
            elif xM == -1 and (x - xIni) <= -1:
                bStuck = False

        if bStuck == True:
            if iDirectinY == 1:
                iReturnMove = RoboCasilla.Move(0, 1, x2, y2)
                if iReturnMove== 0:
                    time.sleep(RoboMoveTime)
                    x, y = RoboCasilla.GetCoord()
                    lienzo_principal.update()
                    iDirectinX = iDirectinXOri

                else:
                    iDirectinY = -iDirectinY

            else:
                iReturnMove = RoboCasilla.Move(0, -1, x2, y2)
                if iReturnMove == 0:
                    time.sleep(RoboMoveTime)
                    x, y = RoboCasilla.GetCoord()
                    lienzo_principal.update()
                    iDirectinX = iDirectinXOri
                else:
                    iDirectinY = -iDirectinY

        if yM != 0:
            if yM == 1 and (y - yIni) >= 1:
                bStuck = False
            elif yM == -1 and (y - yIni) <= -1:
                bStuck = False



def goRobot(x2, y2):

    global RoboCasilla
    global lienzo_principal
    x1 = 0
    y1 = 0

    x1, y1 = RoboCasilla.GetCoord()

    iStepsX = 1
    if y1 != y2:
        iStepsX = abs((x1 - x2) / (y1 - y2))

    iStepsY = 1
    if iStepsX != 0:
        iStepsY = abs(1 / iStepsX)
    x = x1
    y = y1
    x, y = RoboCasilla.GetCoord()

    while (x != x2 or y != y2):

        if iStepsX > 1:
            if x < x2:
                if RoboCasilla.Move(1, 0, x2, y2) == 1:
                    Unstuck(1, 0, x2, y2)
            elif x > x2:
                if RoboCasilla.Move(-1, 0, x2, y2) == 1:
                    Unstuck(-1, 0, x2, y2)
            iStepsX = iStepsX - 1
            time.sleep(RoboMoveTime)
            x, y = RoboCasilla.GetCoord()
            lienzo_principal.update()

        if iStepsY > 1:
            if y < y2:
                if RoboCasilla.Move(0, 1, x2, y2) == 1:
                    Unstuck(0, 1, x2, y2)
            elif y > y2:
                if RoboCasilla.Move(0, -1, x2, y2) == 1:
                    Unstuck(0, -1, x2, y2)


            iStepsY = iStepsY - 1
            time.sleep(RoboMoveTime)
            x, y = RoboCasilla.GetCoord()
            lienzo_principal.update()

        iStepsX = iStepsX + iStepsX
        iStepsY = iStepsY + iStepsY


def ResetTasksBtn():
	set_tasks()

def salir():
	quit(0)

init_app()

mainWin.grid_rowconfigure(0, weight=1)
mainWin.grid_columnconfigure(0, weight=1)
labelStatus = tkinter.Label(mainWin, text="Listo", bg="green", fg="black")
btnStart = tkinter.Button(mainWin, text="Ejecutar", command=funcion)
btnResetTask = tkinter.Button(mainWin, text="Reset Tareas", command=ResetTasksBtn)
btnLimpiar = tkinter.Button(mainWin, text="Limpiar", command=LimpiarBtn)
btnSalir = tkinter.Button(mainWin, text="Salir", command=salir)

labelStatus.grid(row=0, column=0, columnspan=1, sticky=tkinter.W+tkinter.E)
btnStart.grid(row=1, column=0, columnspan=1, sticky=tkinter.W, pady = 2)
btnResetTask.grid(row=2, column=0, columnspan=1, sticky=tkinter.W, pady = 2)
btnLimpiar.grid(row=2, column=1, columnspan=1, sticky=tkinter.W, pady = 2)
btnSalir.grid(row=3, column=0, columnspan=1, sticky=tkinter.W, pady = 2)
lienzo_principal.grid(row=4, column=0, columnspan=1, sticky=tkinter.W, pady = 2)
set_tasks()
mainWin.mainloop()


