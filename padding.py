
import socket

host = "51.38.191.157"
port = 11111

with open("cbc_ciphertext") as f:
    data = bytes.fromhex(f.read().strip())

blocs = [data[i:i+16] for i in range(0, len(data), 16)]


def oracle(message):
    s = socket.create_connection((host, port))
    s.sendall(message.hex().encode() + b"\n")
    reponse = s.recv(4096).decode()
    s.close()
    return "Successfully decrypted" in reponse


resultat = b""

for b in range(1, len(blocs)):
    precedent = blocs[b-1]
    courant = blocs[b]

    inter = [0] * 16
    clair = [0] * 16

    print("\nBloc", b)

    for i in range(15, -1, -1):
        padding = 16 - i

        for valeur in range(256):
            modifie = bytearray(precedent)

            for j in range(i+1, 16):
                modifie[j] = inter[j] ^ padding

            modifie[i] = valeur

            if oracle(modifie + courant):

                if padding == 1:
                    test = bytearray(modifie)
                    test[14] ^= 1
                    if not oracle(test + courant):
                        continue

                inter[i] = valeur ^ padding
                clair[i] = inter[i] ^ precedent[i]

                print(i, ":", hex(clair[i]))
                break
        else:
            print("Octet introuvable")

    resultat += bytes(clair)

padding = resultat[-1]
resultat = resultat[:-padding]

print("\nMessage :", resultat.decode())
