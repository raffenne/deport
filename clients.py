import socket
import os, sys
import time

host, port = ("localhost", 5566)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nomFich = input(" >> Name of the file : ")

if nomFich != "":
            try:
                fich = open(nomFich, "rb")  # test if the file exist
                fich.close()
            except:
                print(" >> the file '" + nomFich + " is nowhere to be found.")
                time.sleep(2)
                exit()

            octets = os.path.getsize(nomFich) / 1024
            print(" >> OK : '" + nomFich + "' [" + str(octets) + " Ko]")
            print("")

            print("")
            print(" >> Connexion to the server is a success, waiting for a response...")
            print("")

            socket.connect((host, port))
            recu = "NAME " + nomFich + " OCTETS " + str(octets)
            socket.send(recu.encode('utf8'))

            while (socket.connect):

                recu = socket.recv(1024)
                recu = recu.decode('utf8')
                if not recu: break

                if recu == "start":  # If the server accepts we send the file
                    print(" >> your request is accepted by the server")
                    print(time.strftime(" >> [%H:%M] transfer in progress please wait..."))
                    print(" ")

                    num = 0
                    pourcent = 0
                    octets = octets * 1024
                    fich = open(nomFich, "rb")

                    if octets > 1024:
                        for i in range(int(octets / 1024)):

                            fich.seek(num,
                                      0)  # you move in relation to the character number (group by 1024 octets)
                            donnees = fich.read(1024)  # Reading the 1024 byte file
                            socket.send(donnees)  # Sending the file in 1024-byte packets
                            num = num + 1024

                            if pourcent == 0 and num > octets / 100 * 10 and num < octets / 100 * 20:
                                print(" -->>                   10%")
                                pourcent = 1
                            elif pourcent == 1 and num > octets / 100 * 20 and num < octets / 100 * 30:
                                print(" ---->>                 20%")
                                pourcent = 2
                            elif pourcent < 3 and num > octets / 100 * 30 and num < octets / 100 * 40:
                                print(" ------>>               30%")
                                pourcent = 3
                            elif pourcent < 4 and num > octets / 100 * 40 and num < octets / 100 * 50:
                                print(" -------->>             40%")
                                pourcent = 4
                            elif pourcent < 5 and num > octets / 100 * 50 and num < octets / 100 * 60:
                                print(" ---------->>           50%")
                                pourcent = 5
                            elif pourcent < 6 and num > octets / 100 * 60 and num < octets / 100 * 70:
                                print(" ------------>>         60%")
                                pourcent = 6
                            elif pourcent < 7 and num > octets / 100 * 70 and num < octets / 100 * 80:
                                print(" -------------->>       70%")
                                pourcent = 7
                            elif pourcent < 8 and num > octets / 100 * 80 and num < octets / 100 * 90:
                                print(" ---------------->>     80%")
                                pourcent = 8
                            elif pourcent < 9 and num > octets / 100 * 90 and num < octets / 100 * 100:
                                print(" ------------------>>   90%")
                                pourcent = 9

                    else:  # Otherwise, we're all going to send out all at once
                        donnees = fich.read()

                        socket.send(donnees)

                    fich.close()
                    print("")
                    print(time.strftime(" >> Le %d/%m a %H:%M transfer completed !"))
                    claque = 'BYE'
                    claque = claque.encode('utf8')
                    socket.send(claque)  # Sending that the transfer is complete

                    #####print('>>waiting for processed files')

                    socket.close()
else:
            print('>>non-existent file')
