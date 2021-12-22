#programme fait dans le cours d'un projet d'inteligence artificiel
# crée par:
#
#
import datetime
import serial
import threading
import keyboard


enMarche = 0  # variable pour savoir si le code est en marche
nom_fichier = "test"
type_rotation = "test2"
timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H%M%S")
print(timestamp)


def menu():  #le menu
    print("[1] rotation vertical droite")
    print("[2] rotation vertical gauche")
    print("[3] rotation horizontal droite")
    print("[4] rotation horizontal gauche")
    print("[5] rotation avant")
    print("[6] rotation arriere")
    print("[0] Quitter le programme")


class MyThread(threading.Thread):

    enExecution = False

    def __init__(self, threadID, type_rotation, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        threading.Thread.__init__(self)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()  # Used to stop the thread identification
        self.__running.set()  # Set running to True
        self.threadID = threadID
        self.type_rotation = type_rotation
        global nom_fichier
        nom_fichier = self.type_rotation + timestamp

    def run(self):
        global enMarche
        global nom_fichier
        self.enExecution = True
        lire_port_serie()

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()
        lire_port_serie()
        print("print de test")


#Le nom du dossier dans la fonction
thread = MyThread(1, type_rotation)


def marche(typeRotation):
    global enMarche
    global type_rotation
    type_rotation = typeRotation
    enMarche = 1
    if not thread.enExecution:
        thread.start()
    else:
        thread.resume()
        print("print dans le marche() pour resume")


def attente():
    #keyboard.release("k")
    print("pesez sur la touche espace pour attenteer le programme")
    while True:  # making a loop
        global enMarche
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('k'):  # if key 'q' is pressed
                print('You Pressed A Key!')
                thread.pause()
                enMarche = 0
                break  # finishing the loop
        except:
            print("autre que la barre espace")
            thread.pause()
            break  # if user pressed a key other than the given key the loop will break


def lire_port_serie():
    portserie = serial.Serial('COM3', baudrate=115200, timeout=2)   #mettre les bonne information ici, cela est imperatif

    f = open("data/" + nom_fichier + ".txt", "a")

    while enMarche == 1:
        donnees_arduino = portserie.readline()
        print(donnees_arduino)
        f.write(donnees_arduino.decode("utf-8"))

    f.close()
    portserie.close()

menu()
option = int(input("entrer la fonction choisie:"))


while option != 0:
    if option == 1:
        marche("rotation_vertical_droite")
        attente()
        option = 0
    elif option == 2:
        marche("rotation_vertical_gauche")
        attente()
        option = 0
    elif option == 3:
        marche("rotation_horizontal_droite")
        attente()
        option = 0
    elif option == 4:
        marche("rotation_horizontal_gauche")
        attente()
        option = 0
    elif option == 5:
        marche("rotation_avant")
        attente()
        option = 0
    elif option == 6:
        marche("rotation_arriere")
        attente()
        option = 0
    else:
        print("voulez quitter le programme")
        print("Le programme va se fermer")