import socket
import threading
import os
import time

my_lock=threading.RLock()#creation of the lock

class ThreadforClients (threading.Thread) :# threadings
    def __init__(self,conn): 
        threading.Thread.__init__(self)
        self.conn=conn

    def run(self):
        with my_lock:
            accepte = "non"
            num = 0
            pourcent = 0

            while conn.connect:
                recu = conn.recv(1024)#message received from the client in bytes
                recu = recu.decode('utf8')

                if not recu: break

                if accepte == "non":  # Condition if we haven't already sent the name and size of the file.
                    nomFich = recu.split("NAME ")[1]
                    nomFich = nomFich.split("OCTETS ")[0]
                    taille = recu.split("OCTETS ")[1]
                    print(" >> Fichier \'" + nomFich + "\' [" + taille + " Ko]")
                    accepte = input(" >> do you accept the transfert [o/n] : ")

                    if accepte == "o" or accepte == "oui" or accepte == "yes":  # Si oui en lenvoi au client et on cree le fichier
                        nomFich=nomFich[0:(len(nomFich)-5)]
                        lalal="start"
                        lalal=lalal.encode('utf8')
                        conn.send(lalal)
                        try :#creation of a gerard file containing the sent file
                            os.mkdir('gerard', 0o777)
                        except FileExistsError:
                            print('')
                        fd=os.open("gerard/" + nomFich + ".csv",os.O_RDWR|os.O_CREAT)
                        fo = os.fdopen(fd, "w+")
                        print(time.strftime(" >> [%H:%M] transfert en cours veuillez patienter..."))
                        print("")
                        taille = float(taille) * 1024  # Conversion de la taille en octets pour le %

                    else:
                        lola='Bye'
                        lola=lola.encode('utf8')
                        conn.send(lola)  
                        exit()

                elif recu == "BYE":  
                    fo.close()
                    print("")
                    print(time.strftime(" >> Le %d/%m a %H:%M transfert termine !"))


                else:  
                    fo.write( recu)


                    if taille > 1024:  

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
            



        print('it is finished you have all the files')


#-------------------------------------------- Launching the server

host, port = ('', 5566)

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.bind((host,port))
print('>>The server is up and waiting for clients')

while True:

    socket.listen(100)
    conn, adresse = socket.accept()
    myThread = ThreadforClients(conn)
    myThread.start()
    myThread.join()


socket.close()
