from socket import *
import time
serverName = "192.168.130.101"
serverPort = 1300
geraLogsDebug = True

# def ordem_no_alfabeto(letra):
#     if letra.isupper():
#         return ord(letra) - ord('A') + 1
#     elif letra.islower():
#         return ord(letra) - ord('a') + 1
#     else:
#         return 0  # Se não for uma letra do alfabeto
    
# def letra_no_alfabeto(posicao):
#     if 1 <= posicao <= 26:  # O alfabeto tem 26 letras
#         return chr(ord('A') + posicao - 1)
#     else:
#         return ' '  # Se a posição estiver fora do intervalo válido

# def trocaLetra(letra):
#     posicaoLetraAlfabeto = ordem_no_alfabeto(letra)
#     chave = pow(posicaoLetraAlfabeto, int(e), int(n))
#     print("antes:", posicaoLetraAlfabeto)
#     print("depois:", chave)
#     a = letra_no_alfabeto(chave)
#     return letra_no_alfabeto(chave)

# def cript(texto):
#     textoAlterado = ""
#     for caract in texto:
#         textoAlterado += trocaLetra(caract)
#     return textoAlterado

def encrypt(message, e, n):
    #message_int = int.from_bytes(message.encode(), byteorder='big')
    
    numeroTexto = ""
    for caract in message:
        numeroTexto += str(ord(caract))
    
    encrypted = pow(int(numeroTexto), int(e), int(n))
    return encrypted

def abreSocket():
    clientSocket.connect((serverName, serverPort))

def fechaSocket():
    clientSocket.close()

def recebeDado():
    recebido = clientSocket.recv(65000)
    return str(recebido,"utf-8")

def realizaLog(msg):
    if(geraLogsDebug):
        print (msg)

clientSocket = socket(AF_INET, SOCK_STREAM)

abreSocket()

chavePublica = recebeDado()
realizaLog ("Recebi a chave: " + chavePublica)
chavePublica = chavePublica.replace('(','').replace(')','')

chaves = chavePublica.split(',')
e = chaves[0]
n = chaves[1]

# msg = "The information security is of significant importance to ensure the privacy of communications"
msg="the"
msgCript = encrypt(msg, e, n)
realizaLog ("Mensagem original: " + msg)
realizaLog ("Mensagem criptografada enviada: " + str(msgCript))
clientSocket.send(bytes(str(msgCript), "utf-8"))
time.sleep(1)

mensagemMaiuscula = recebeDado()
print ("Mensagem devolvida pelo server: " + mensagemMaiuscula)

fechaSocket()
