from socket import *
from Crypto.Util import number
import datetime
import time
import random
import math
serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
geraLogsDebugs = False
p = 0
q = 0
tamanhoBitsNroPrimo = 1024 # Número de bits do primo
rnd = number.getRandomNumber # Função aleatória para gerar os números


def abreSocket():
    serverSocket.bind(("",serverPort))
    serverSocket.listen(5) # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5 requisições de conexão (normalmente o máximo) antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.

def fechaSocket():
    connectionSocket.close()

def enviaDado(dado):
    connectionSocket.send(bytes(str(dado), "utf-8"))

def recebeDado():
    msg = connectionSocket.recv(65000)
    return str(msg,"utf-8")


def geraNumeroPrimo(bit_length, rnd):
    return number.getPrime(bit_length, randfunc=rnd)



def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def geraParChaves(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Escolher um número inteiro e tal que seja coprimo com phi
    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break
    
    # Calcular o inverso multiplicativo de e mod phi
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def mod_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

def encrypt(public_key, mensagem):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in mensagem]
    return cipher

def decrypt(private_key, cipher):
    d, n = private_key
    mensagem = [chr(pow(char, d, n)) for char in cipher]
    return ''.join(mensagem)


def testeRSA():
    p = geraNumeroPrimo(tamanhoBitsNroPrimo,rnd=rnd)
    q = geraNumeroPrimo(tamanhoBitsNroPrimo,rnd=rnd)

    public_key, private_key = geraParChaves(p, q)
    
    mensagem = "Hello, World!"
    print("Mensagem original:", mensagem)
    
    cipher = encrypt(public_key, mensagem)
    print("Mensagem cifrada:", ''.join(map(lambda x: str(x), cipher)))
    
    decrypted_message = decrypt(private_key, cipher)
    print("Mensagem decifrada:", decrypted_message)

def realizaLog(msg):
    if (geraLogsDebugs):
        print(msg)

clientSocket = socket(AF_INET, SOCK_STREAM)


print ("TCP Server em Execução")

abreSocket()
connectionSocket, addr = serverSocket.accept()

#msgCript = connectionSocket.recv(65000)
#msgCriptUnicode = str(msgCript,"utf-8")

#devolveMaiusculo = msg.upper()
#msgCriptoMaiusculo = criptDecript(devolveMaiusculo,K,False)
#enviaDado(msgCriptoMaiusculo)
#realizaLog("Mensagem criptografada recebida: " + msgCriptUnicode)

#print ("Mensagem decriptografada : ", msg)
#print ("Mensagem devolvida para o client : ", devolveMaiusculo)


fechaSocket()
