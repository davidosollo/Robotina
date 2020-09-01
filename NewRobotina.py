"""
  Institucion:  Universidad Autonoma de Guadalajara (UAG)
  Nombre:       David Osollo, Enrique Martinez
  Proyecto:     Proyecto Robotina
  Materia:      Computacion Cognitiva

  Descripicion: El programa consiste en una Robotina que haga las tareas del hogar,
                cuide de no descargarse, decidir las secuencia de las tareas en base
                a un entrenamiento de una red Neural con la informacion de como la
                señora de la casa prioritizo las tareas durante 50 dias. En base a
                ese entrenmiento se toma la descicion en que orden se realizaran las
                tareas.
"""


import tkinter # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from tkinter.ttk import *
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import pandas as pd
import random
import time
import math
from tensorflow import keras


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
imgPlan = None
photoPlan = None
progressEnergy = None
progressSleep = None
model = None
sRed = None
sBlue = None
task_desc = None
imgObs = None #EMS
photoObs = None #EMS


RoboMoveTime = 0.15
RoboMoveLimpiaTime = 1.5
bLimpio = False

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

        aplicaEnergy(1)

        return 0

    def GetCoord(self):
        return (self.col, self.ren)

    def Limpiar(self, imgClean):
        self.canvas.itemconfig(self.id, image=imgClean)

    def GetTipo(self):
        return self.tipo_casilla


#GetSect
def getSec(npPercentage):

    TaskSec = np.array([])
    pdNoSort = np.reshape(npPercentage, 4)
    pdSort  = np.copy(-np.sort(-npPercentage))
    pdSort = np.reshape(pdSort , 4)

    for task in pdSort:
        i = 0
        for Percent in pdNoSort:
            if task == Percent:
                TaskSec = np.append(TaskSec,i)
                break
            i = i + 1
    return TaskSec


#Construccion del Modelo
def build_model(xSize):

  global model

  model = keras.Sequential()
  model.add(keras.layers.Dense(32, kernel_initializer='glorot_uniform',
                               activation='relu', input_shape=xSize))
  model.add(keras.layers.Dropout(0.2))
  model.add(keras.layers.Dense(120, activation='tanh'))
  model.add(keras.layers.Dense(4, activation='softmax'))

  model.compile(loss='mean_squared_error',
                optimizer=keras.optimizers.Adam())

  return  model



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
    global imgPlan
    global photoPlan
    global image_to_show
    global imgCocinaHerr
    global photoCocinaHerr
    global imgEscoba
    global photoEscoba
    global imgLimpBano
    global photoLimpBano
    global imgLimpio
    global photoLimpio
    global model
    global target_names
    global task_desc
    global imgObs #EMS
    global photoObs #EMS

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

    #imgPlancha = Image.open("./img/plancha.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    #photoPlancha = ImageTk.PhotoImage(imgPlanchar)

    imgPlan = Image.open("./img/plancha.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoPlan = ImageTk.PhotoImage(imgPlan)

    #Imagenes Recargar
    imgCama = Image.open("./img/cama.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoCama = ImageTk.PhotoImage(imgCama)

    imgPila = Image.open("./img/pila.png").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoPila = ImageTk.PhotoImage(imgPila)

    #Imagenes Herramientas

    imgCocinaHerr = Image.open("./img/cocina_herr.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoCocinaHerr = ImageTk.PhotoImage(imgCocinaHerr)

    imgEscoba = Image.open("./img/escoba.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoEscoba = ImageTk.PhotoImage(imgEscoba)

    imgLimpBano = Image.open("./img/limpiabanos.jpg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoLimpBano = ImageTk.PhotoImage(imgLimpBano)

    imgLimpio = Image.open("./img/limpio.jpeg").resize((frame_size, frame_size), Image.ANTIALIAS)
    photoLimpio = ImageTk.PhotoImage(imgLimpio)

    #imagen de obstaculo
    imgObs = Image.open("./img/obstaculo.png").resize((frame_size, frame_size), Image.ANTIALIAS) #EMS
    photoObs = ImageTk.PhotoImage(imgObs) #EMS

    task_desc = ['LIMPIAR_CASA', 'PLANCHAR', 'COCINAR',  'LIMPIAR BAÑOS']

    #Inicialización Red Neural

    dfRobo = pd.read_excel('./DataSets/RoboCogni.xlsx')

    X = dfRobo[dfRobo.columns[0:4]].to_numpy()
    Y = dfRobo[dfRobo.columns[4:]].to_numpy()

    X = X / X.max(axis=0)

    print(X.shape)
    print(Y.shape)

    # Construir el Modelo
    model = build_model([X.shape[1]])

    X = np.asarray(X).astype(np.float32)
    Y = np.asarray(Y).astype(np.float32)

    # Entrenar el Modelo
    history = model.fit(X, Y,
                        batch_size=150, epochs=100,
                        validation_split=0.2, verbose=1)

    model.summary()

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
    global imgPlan
    global photoPlan
    global RoboCasilla
    global arr_tareas
    global RoboTrayectoria
    global imgObs #EMS
    global photoObs #EMS

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
            elif col == 12 and ren == 0:
                image_to_show = photoPlan
                Tipo_Casilla = 6
            else:
                tarea = random.randint(1, 40)
                if ren == 0 or ren == 1:
                    image_to_show = photoCuadroAmarillo
                    Tipo_Casilla = 0

                if ren != 0 and ren != 1:
                    if tarea == 1 and np.count_nonzero(arr_tareas == tarea) < 2:
                        image_to_show = photoBasura
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 7
                    elif tarea == 2 and np.count_nonzero(arr_tareas == tarea) < 2:
                        image_to_show = photoPlanchar
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 8
                    elif tarea == 3 and np.count_nonzero(arr_tareas == tarea) < 2:
                        image_to_show = photoCocinar
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 9
                    elif tarea == 4 and np.count_nonzero(arr_tareas == tarea) < 2:
                        image_to_show = photoToilet
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 10
                    elif tarea == 5 or tarea == 20: #EMS
                        image_to_show = photoObs
                        arr_tareas = np.append(arr_tareas, tarea)
                        Tipo_Casilla = 11

                    else:
                        image_to_show = photoCuadroAzul
                        Tipo_Casilla = 0

            casilla = casilla_frame(lienzo_principal, Tipo_Casilla, col, ren, frame_size, offset_y, offset_x, init_color,
                                    image_to_show)

            if (Tipo_Casilla >= 1) and (Tipo_Casilla <=6):
                casillas_tareas_map[casilla.id] = casilla
            elif (Tipo_Casilla >= 7) and (Tipo_Casilla <=11):
                casillas_tareas_map[casilla.id] = casilla

    image_to_show = photoRobotina
    RoboCasilla = casilla_frame(lienzo_principal, 10, 0, 0, frame_size, offset_y, offset_x, init_color, image_to_show)

def aplicaEnergy(iCantidad):
    global sRed
    global progressEnergy

    if progressEnergy['value'] != 0:
        progressEnergy['value'] = progressEnergy['value'] - iCantidad
        sRed.configure('red.Horizontal.TProgressbar',
                       text='Bateria {:g} %'.format(progressEnergy['value']))

def cargaEnergy(iCantidad):
    global sRed
    global progressEnergy

    progressEnergy['value'] = progressEnergy['value'] + iCantidad
    sRed.configure('red.Horizontal.TProgressbar',
                    text='Bateria {:g} %'.format(progressEnergy['value']))

    if progressEnergy['value'] > 100:
        progressEnergy['value'] = 100


def funcion():
	print('Exelente')

def EjecutarBtn():
    RoboLimpia()

def RoboLimpia():

    global bLimpio
    global model

    ListaTask = " : "


    olor_casa = random.random()
    tiempo_trabajo = random.random()
    hambre = random.random()
    olor_baño = random.random()

    xTest = np.array([[olor_casa, tiempo_trabajo, hambre, olor_baño]])
    results = model.predict(xTest)
    RoboSecs = getSec(results)

    if bLimpio == True:
        set_tasks()

    for tarea in RoboSecs:
        ListaTask =  ListaTask + " - " + task_desc[int(tarea)]

    labelStatus.configure(background="yellow")
    labelStatus.configure(foreground="red")
    labelStatus.configure(text = "Limpiando" + ListaTask)
    lienzo_principal.update()
    # Checar si esta ocupado

    for TipoTask in RoboSecs:

        if TipoTask == 0:
            ReviewCharge(8, 0)
            goRobot(8, 1)
            goRobot(8, 0)
        elif TipoTask == 1:
            ReviewCharge(12, 0)
            goRobot(12, 1)
            goRobot(12, 0)
        elif TipoTask == 2:
            ReviewCharge(6, 0)
            goRobot(6, 1)
            goRobot(6, 0)
        else:
            ReviewCharge(10, 0)
            goRobot(10, 1)
            goRobot(10, 0)

        time.sleep(1)

        for tarea in casillas_tareas_map:
            if casillas_tareas_map[tarea].GetTipo() == (TipoTask + 7):
                x, y = casillas_tareas_map[tarea].GetCoord()
                ReviewCharge(x, y)
                goRobot(x, y)
                for i in range(1, 5):
                    time.sleep(1)
                    aplicaEnergy(1)
                    lienzo_principal.update()

                casillas_tareas_map[tarea].Limpiar(photoLimpio)

    ReviewCharge(0, 0)
    goRobot(1, 1)
    goRobot(0, 0)

    labelStatus.configure(background="green")
    labelStatus.configure(foreground="white")
    labelStatus.configure(text="Listo")
    lienzo_principal.update()
    bLimpio = True


def ReviewCharge(xNextTask, yNextTask):


    ret = 0
    iRoboX, iRoboY = RoboCasilla.GetCoord()

    iDistancia = math.sqrt(math.pow((xNextTask - iRoboX), 2) + math.pow((yNextTask - iRoboY), 2)) + 3
    iDistancia = iDistancia + math.sqrt(math.pow((2 - iRoboX),2) + math.pow((0 -iRoboY),2))
    iDistancia = iDistancia + (iDistancia * .10)

    if progressEnergy['value'] < iDistancia:
        goRobot(2, 1)
        goRobot(2, 0)
        ret = 1
        while progressEnergy['value'] < 100:
            time.sleep(1)
            cargaEnergy(20)
            lienzo_principal.update()

    return ret

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

        if x == x2 and y == y2:
            break

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

        if x == x2 and y == y2:
            break

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

        #if iStepsX > 1:
        if x < x2:
            if RoboCasilla.Move(1, 0, x2, y2) == 1:
                Unstuck(1, 0, x2, y2)
                if y != y2:
                    iStepsX = abs((x - x2) / (y - y2))
                if iStepsX != 0:
                    iStepsY = abs(1 / iStepsX)
        elif x > x2:
            if RoboCasilla.Move(-1, 0, x2, y2) == 1:
                Unstuck(-1, 0, x2, y2)
                if y != y2:
                    iStepsX = abs((x - x2) / (y - y2))
                if iStepsX != 0:
                    iStepsY = abs(1 / iStepsX)
        iStepsX = iStepsX - 1
        time.sleep(RoboMoveTime)
        x, y = RoboCasilla.GetCoord()
        lienzo_principal.update()

        #if iStepsY > 1:
        if y < y2:
            if RoboCasilla.Move(0, 1, x2, y2) == 1:
                Unstuck(0, 1, x2, y2)
                if y != y2:
                    iStepsX = abs((x - x2) / (y - y2))
                if iStepsX != 0:
                    iStepsY = abs(1 / iStepsX)
        elif y > y2:
            if RoboCasilla.Move(0, -1, x2, y2) == 1:
                Unstuck(0, -1, x2, y2)
                if y != y2:
                    iStepsX = abs((x - x2) / (y - y2))
                if iStepsX != 0:
                    iStepsY = abs(1 / iStepsX)


            iStepsY = iStepsY - 1
            time.sleep(RoboMoveTime)
            x, y = RoboCasilla.GetCoord()
            lienzo_principal.update()

        iStepsX = iStepsX + iStepsX
        iStepsY = iStepsY + iStepsY


def ResetTasksBtn():

    global bLimpio

    set_tasks()
    bLimpio = False


def salir():
	quit(0)

init_app()

mainWin.grid_rowconfigure(0, weight=1)
mainWin.grid_columnconfigure(0, weight=1)
labelStatus = tkinter.Label(mainWin, text="Listo", bg="green", fg="white")
btnStart = tkinter.Button(mainWin, text="Ejecutar", command=EjecutarBtn)
btnResetTask = tkinter.Button(mainWin, text="Reset Tareas", command=ResetTasksBtn)
btnSalir = tkinter.Button(mainWin, text="Salir", command=salir)

sRed = tkinter.ttk.Style()

variable = tkinter.DoubleVar(mainWin)

sRed.layout('red.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
#sRed.theme_use('clam')
sRed.configure("red.Horizontal.TProgressbar", foreground='white', background='red', text='0 %')

sBlue = tkinter.ttk.Style()
sBlue.layout('blue.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
#sBlue.theme_use('clam')
sBlue.configure("blue.Horizontal.TProgressbar", foreground='blue', background='cyan', text='0 %')

progressEnergy = Progressbar(mainWin, style="red.Horizontal.TProgressbar",orient=HORIZONTAL, length=100, mode='determinate')
progressEnergy['value'] = 100

sBlue.configure('blue.Horizontal.TProgressbar',
                text='Sueño {:g} %'.format(progressEnergy['value']))

progressSleep = Progressbar(mainWin, style="blue.Horizontal.TProgressbar",orient=HORIZONTAL, length=100, mode='determinate')
progressSleep['value'] = 100

sRed.configure('red.Horizontal.TProgressbar',
                text='Bateria {:g} %'.format(progressEnergy['value']))


labelStatus.grid(row=0, column=0, columnspan=1, sticky=tkinter.W+tkinter.E)
progressSleep.grid(row=1, column=0, columnspan=1, sticky=tkinter.W+tkinter.E)
progressEnergy.grid(row=2, column=0, columnspan=1, sticky=tkinter.W+tkinter.E)

btnStart.grid(row=3, column=0, columnspan=1, sticky=tkinter.W, pady = 2)
btnResetTask.grid(row=4, column=0, columnspan=1, sticky=tkinter.W, pady = 2)
btnSalir.grid(row=5, column=0, columnspan=1, sticky=tkinter.W, pady = 2)

lienzo_principal.grid(row=6, column=0, columnspan=1, sticky=tkinter.W, pady = 2)

set_tasks()
mainWin.mainloop()


