from socket import *
import datetime
serverName = "10.1.70.22"
serverPort = 1300
geraLogsDebug = False

def abreSocket():
    clientSocket.connect((serverName, serverPort))

def fechaSocket():
    clientSocket.close()

def enviaR2(R2):
    clientSocket.send(bytes(str(R2), "utf-8"))

def recebeDado():
    recebido = clientSocket.recv(65000)
    return str(recebido,"utf-8")

def trocaLetra(letra,chave):
    nroLetra = ord(letra) + chave
    return chr(nroLetra)

def criptDecript(texto,chave,decript):
    textoAlterado = ""
    if (decript): 
        chave = -chave

    for caract in texto:
            textoAlterado += trocaLetra(caract,chave)
    return textoAlterado

def obtemChaveDiffieHellmann():
    R2 = (G ** Y) % N
    enviaR2(R2)
    realizaLog ("enviou R2 " + str(R2) + " | " + str(datetime.datetime.now()))
    R1 = recebeDado()
    realizaLog ("recebeu R1 " + str(R1) + " | " + str(datetime.datetime.now()))
    K = (int(R1) ** Y) % N
    realizaLog ("K: " + str(K))
    return K

def realizaLog(msg):
    if(geraLogsDebug):
        print (msg)

clientSocket = socket(AF_INET, SOCK_STREAM)
G = 11
N = 23
Y = 1340000

abreSocket()

K = obtemChaveDiffieHellmann()

msg = input("Mande uma mensagem: ")
msgCript = criptDecript(msg, K, False)
realizaLog ("Mensagem original: " + msg)
realizaLog ("Mensagem criptografada enviada: " + msgCript)
clientSocket.send(bytes(msgCript, "utf-8"))

mensagemMaiuscula = recebeDado()
msgDecript = criptDecript(mensagemMaiuscula, K, True)
print ("Mensagem devolvida pelo server: " + msgDecript)

fechaSocket()

