import socket, string

HOST = "51.38.191.157"
PORT = 4321

def recup_chiffree():
    with socket.create_connection((HOST, PORT)) as s:
        morceau = s.recv(1024)
    chiffre = morceau.decode()
    return chiffre

tab_ch = []
for i in range(200):
    tab_ch.append(recup_chiffree())

print(len(tab_ch))
tab_pos = []
for i in range(18):
    s = set()
    for j in range(200):
        s.add(tab_ch[j][i])
    tab_pos.append(s)

msg_secret=""
alphabet = string.ascii_uppercase
for i in range(18):
    c, = set(alphabet) - tab_pos[i]
    msg_secret += c



print(msg_secret)  #LACRYPTOCESTGENIAL