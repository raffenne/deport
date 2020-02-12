import socket
import threading
import os
import time

my_lock=threading.RLock()#creation du verrou expliquer plus tard

class ThreadforClients (threading.Thread) :#la classe threading permet d'eviter des problemes de lag lorsqu'il y a trop de clients

    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn=conn

    def run(self):
        with my_lock:#si plusieurs clients les taches ne se font pas en parallèle mais un client apres lautre
            accepte = "non"
            num = 0
            pourcent = 0

            while conn.connect:
                recu = conn.recv(1024)#message capte du client en bytes
                recu = recu.decode('utf8')

                if not recu: break

                if accepte == "non":  # Condition si on a pas deja envoyer le nom et la taille du fichier
                    nomFich = recu.split("NAME ")[1]
                    nomFich = nomFich.split("OCTETS ")[0]
                    taille = recu.split("OCTETS ")[1]
                    print(" >> Fichier \'" + nomFich + "\' [" + taille + " Ko]")
                    accepte = input(" >> Acceptez vous le transfert [o/n] : ")

                    if accepte == "o" or accepte == "oui" or accepte == "yes":  # Si oui en lenvoi au client et on cree le fichier
                        nomFich=nomFich[0:(len(nomFich)-5)]
                        lalal="GO"
                        lalal=lalal.encode('utf8')
                        conn.send(lalal)
                        try :#creation d'un fichier gerard qui contient le fichier envoye
                            os.mkdir('gerard', 0o777)
                        except FileExistsError:
                            print('')
                        fd=os.open("gerard/" + nomFich + ".csv",os.O_RDWR|os.O_CREAT)#le fichier est cree et est pret à etre ecrits
                        fo = os.fdopen(fd, "w+")#creation de l'objet fichier pour que l'ordinateur comprenne ... j'ai essayé pas mal de truc avec la bibliotheque os c'est le seul truc qui marche
                        print(time.strftime(" >> [%H:%M] transfert en cours veuillez patienter..."))#la bilitohèque time permet d'ajouter des informations sur l'heure en temps réel (souvent utilisé pour complété des logs de tous les niveaux)
                        print("")
                        taille = float(taille) * 1024  # Conversion de la taille en octets pour le %

                    else:
                        lola='Bye'
                        lola=lola.encode('utf8')
                        conn.send(lola)  # Si pas accepte on ferme le programme
                        exit()

                elif recu == "BYE":  # Si on a recu "BYE" le transfer est termine
                    fo.close()
                    print("")
                    print(time.strftime(" >> Le %d/%m a %H:%M transfert termine !"))


                else:  # Sinon on ecrit au fur et a mesure dans le fichier
                    fo.write( recu)


                    if taille > 1024:  # Si la taille est plus grande que 1024 on s'occupe du %

                        # Condition pour afficher le % du transfert :
                        if pourcent == 0 and num > taille / 100 * 10 and num < taille / 100 * 20:
                            print(" -->>                   10%")
                            pourcent = 1
                        elif pourcent == 1 and num > taille / 100 * 20 and num < taille / 100 * 30:
                            print(" ---->>                 20%")
                            pourcent = 2
                        elif pourcent < 3 and num > taille / 100 * 30 and num < taille / 100 * 40:
                            print(" ------>>               30%")
                            pourcent = 3
                        elif pourcent < 4 and num > taille / 100 * 40 and num < taille / 100 * 50:
                            print(" -------->>             40%")
                            pourcent = 4
                        elif pourcent < 5 and num > taille / 100 * 50 and num < taille / 100 * 60:
                            print(" ---------->>           50%")
                            pourcent = 5
                        elif pourcent < 6 and num > taille / 100 * 60 and num < taille / 100 * 70:
                            print(" ------------>>         60%")
                            pourcent = 6
                        elif pourcent < 7 and num > taille / 100 * 70 and num < taille / 100 * 80:
                            print(" -------------->>       70%")
                            pourcent = 7
                        elif pourcent < 8 and num > taille / 100 * 80 and num < taille / 100 * 90:
                            print(" ---------------->>     80%")
                            pourcent = 8
                        elif pourcent < 9 and num > taille / 100 * 90 and num < taille / 100 * 100:
                            print(" ------------------>>   90%")
                            pourcent = 9

                        num = num + 1024
            #creation du fichier
            #path='gerard/' + nomFich + '.csv'

            #try :
             #   os.mkdir('gerard/fichiers_traites', 0o777)
            #except FileExistsError:
             #    print('')
            #fq = os.open("gerard/" + nomFich + "_traite.csv", os.O_RDWR | os.O_CREAT)




        print('c\'est fini, tu as tous les fichiers')


#--------------------------------------------

host, port = ('', 5566)

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.bind((host,port))
print('>>Le server est en marche et attend des clients')

while True:

    socket.listen(5)#on autorise le serveur à refuser 5 connections
    conn, adresse = socket.accept()#on accepte le client ... ca n'est pas très securise mais j'y travaille
    myThread = ThreadforClients(conn)#
    myThread.start()
    myThread.join()


socket.close()
