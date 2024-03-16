from socket import *
import time
from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes
serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
geraLogsDebugs = True
encode = "utf-8"
bitLength = 8

def abreSocket():
    serverSocket.bind(("",serverPort))
    serverSocket.listen(5) # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5 requisições de conexão (normalmente o máximo) antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.

def enviaDado(dado, encode):
    connectionSocket.send(bytes(str(dado),encode))

def recebeDado(encode):
    msgRaw = connectionSocket.recv(65000)
    return str(msgRaw,encode)

def fechaSocket():
    connectionSocket.close()

def encrypt(message, e, n, encode):
    vetorEncrypt = []
    for a in message:
        vetorEncrypt.append(int.from_bytes(a.encode(encode)))

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
    if (geraLogsDebugs):
        print(msg)


clientSocket = socket(AF_INET, SOCK_STREAM)

print ("TCP Server em Execução")

abreSocket()
connectionSocket, addr = serverSocket.accept()

###################################

# Escolha aleatória de dois números primos grandes p e q
p = number.getPrime(bitLength // 2)
q = number.getPrime(bitLength // 2)


n = p * q

# função totiente
m = (p - 1) * (q - 1)

# Escolha de um inteiro "e", 1 < "e" < totiente, "e" e totiente devem ser primos entre si
e = m - 1
while number.GCD(m, e) > 1:
    e += 2

d = pow(e, -1, m)

realizaLog("p: "+str(p))
realizaLog("q: "+str(q))
realizaLog("n: "+str(n))
realizaLog("m: "+str(m))
realizaLog("e: "+str(e))
realizaLog("d: "+str(d))

chave =  "(" + str(e) + "," + str(n) + ")"
print("Chave enviada: e e n: "+chave)

############# ENVIA CHAVE ###############

enviaDado(chave, encode)
time.sleep(1)

############# RECEBE MENSAGEM ###############
msgCript = recebeDado(encode)
time.sleep(1)

############# DECRIPTOGRAFA ###############
msgRecv = decrypt(msgCript, d, n)
print("#################")
print("mensagem decrypt: ", msgRecv)
print("#################")

############# RECEBE CHAVE ###############
chavePublicaCliente = recebeDado(encode)
realizaLog ("Recebi a chave: " + chavePublicaCliente)
chavePublicaCliente = chavePublicaCliente.replace('(','').replace(')','')
chaves = chavePublicaCliente.split(',')
e_client = chaves[0]
n_cliente = chaves[1]

############# CRIPTOGRAFA DEVOLUTIVA ###############
devolveMaiusculo = msgRecv.upper()
msgCriptoMaiusculo = encrypt(devolveMaiusculo,int(e_client),int(n),encode)

############# ENVIA MENSAGEM ###############
enviaDado(msgCriptoMaiusculo,encode)
time.sleep(1)
fechaSocket()
