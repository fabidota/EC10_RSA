from socket import *
import time
from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes
import numpy as np
serverName = "10.1.70.22"
serverPort = 1305
geraLogsDebug = True
encode = "utf-8"
bitLength = 8

def enviaDado(dado, encode):
    clientSocket.send(bytes(str(dado),encode))

def recebeDado(encode):
    msgRaw = clientSocket.recv(65000)
    return str(msgRaw,encode)

def encrypt(message, e, n, encode):
    vetorEncrypt = []
    for a in message:
        vetorEncrypt.append(int.from_bytes(a.encode(encode),"big"))

    #print("Vetor de chars encrypt: " + str(vetorEncrypt))
    vetorNumChar = []
    for caract in message:
        vetorNumChar.append(str(pow(ord(caract),int(e),int(n))))

    retorno = ""
    for a in vetorNumChar:
        retorno += chr(int(a))
            
    return retorno

def decrypt(message, d, n):

    vetorDecrypt = []

    for a in message:
        vetorDecrypt.append(str(pow(ord(a),int(d),int(n))))

    saida = ""
    for a in vetorDecrypt:
        saida += chr(int(a))

    return saida

def realizaLog(msg):
    if (geraLogsDebug):
        print(msg)

def abreSocket():
    clientSocket.connect((serverName, serverPort))

def fechaSocket():
    clientSocket.close()


clientSocket = socket(AF_INET, SOCK_STREAM)

abreSocket()
print("Conectado no servidor!!!")

############# RECEBE CHAVE ###############
chavePublica = recebeDado(encode)
realizaLog ("Recebi a chave: " + chavePublica)
chavePublica = chavePublica.replace('(','').replace(')','')

chaves = chavePublica.split(',')
e_server = chaves[0]
n_server = chaves[1]

############# CRIPTOGRAFA MENSAGEM ###############
msg = "The information security is of significant importance to ensure the privacy of communications"
#msg="the"
msgCript = encrypt(msg, int(e_server), int(n_server), encode)
realizaLog ("Mensagem original: " + msg)
realizaLog ("Mensagem criptografada enviada: " + str(msgCript))

############# ENVIA MENSAGEM ###############
enviaDado(msgCript, encode)
time.sleep(1)


###################################

# Escolha aleatória de dois números primos grandes p e q
p = number.getPrime(bitLength // 2)
q = number.getPrime(bitLength // 2)
#p = 17
#q = 23


# função totiente
m = (p - 1) * (q - 1)

# Escolha de um inteiro "e", 1 < "e" < totiente, "e" e totiente devem ser primos entre si
e = m - 1
while number.GCD(m, e) > 1:
    e += 2

d = pow(e, -1, m)

realizaLog("p: "+str(p))
realizaLog("q: "+str(q))
realizaLog("n: "+str(n_server))
realizaLog("m: "+str(m))
realizaLog("e: "+str(e))
realizaLog("d: "+str(d))

############# ENVIA CHAVE ###############
chave =  "(" + str(e) + "," + str(n_server) + ")"
print("Chave enviada: e e n: "+chave)
enviaDado(chave,encode)
time.sleep(1)

############# RECEBE MENSAGEM ###############
mensagemMaiuscula = recebeDado(encode)
time.sleep(1)

############# DECRIPTOGRAFA ###############
msgRecv = decrypt(mensagemMaiuscula, d, int(n_server))
print("#################")
print("mensagem decrypt: ", msgRecv)
print("#################")


#print ("Mensagem devolvida pelo server: " + mensagemMaiuscula)

fechaSocket()
