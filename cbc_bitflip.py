
import socket
import re


def xor(a, b):
    resultat = []

    for i in range(len(a)):
        resultat.append(a[i] ^ b[i])

    return bytes(resultat)


def recevoir_jusqua(s, texte):
    donnees = b""

    while texte not in donnees:
        morceau = s.recv(4096)

        if not morceau:
            raise ConnectionError("Connexion fermee")

        donnees += morceau

    return donnees


# Donnees de l'authentification observee
ancien_challenge = bytes.fromhex(
    "8c9f02f515584b12199c009d24963e5e"
)

ancien_iv = bytes.fromhex(
    "68ff99332c6371adb1a4f5248d5f6ba1"
)

ciphertext = bytes.fromhex(
    "4059350949f275df86c429854ca1933f"
    "b011ed1542f684a4b04312b1d233a821"
)


# Connexion au serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("51.38.191.157", 23403))


# Choisir l'option 2
recevoir_jusqua(s, b"Your choice :")
s.sendall(b"2\n")


# Recuperer le nouveau challenge
reponse = recevoir_jusqua(s, b"Now please give your IV")

print(reponse.decode(errors="replace"))

match = re.search(
    rb"Here is your challenge\s*:\s*([0-9a-fA-F]{32})",
    reponse
)

nouveau_challenge = bytes.fromhex(
    match.group(1).decode()
)


# Calculer le nouvel IV
nouvel_iv = xor(
    xor(ancien_iv, ancien_challenge),
    nouveau_challenge
)

print("Nouvel IV :", nouvel_iv.hex())


# Envoyer le nouvel IV
s.sendall(nouvel_iv.hex().encode() + b"\n")


# Envoyer le ciphertext original
recevoir_jusqua(s, b"ciphertext")
s.sendall(ciphertext.hex().encode() + b"\n")


# Afficher la reponse du serveur
while True:
    reponse = s.recv(4096)

    if not reponse:
        break

    print(reponse.decode(errors="replace"))


# Fermer la connexion
s.close()
