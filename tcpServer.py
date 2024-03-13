from socket import *
import time
from Crypto.Util import number
serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
geraLogsDebugs = False

def abreSocket():
    serverSocket.bind(("",serverPort))
    serverSocket.listen(5) # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5 requisições de conexão (normalmente o máximo) antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.

def enviaDado(dado):
    connectionSocket.send(bytes(str(dado), "utf-8"))

def fechaSocket():
    connectionSocket.close()

def ordem_no_alfabeto(letra):
    if letra.isupper():
        return ord(letra) - ord('A') + 1
    elif letra.islower():
        return ord(letra) - ord('a') + 1
    else:
        return 0  # Se não for uma letra do alfabeto
    
def letra_no_alfabeto(posicao):
    if 1 <= posicao <= 26:  # O alfabeto tem 26 letras
        return chr(ord('A') + posicao - 1)
    else:
        return ' '  # Se a posição estiver fora do intervalo válido

def trocaLetra(letra):
    posicaoLetraAlfabeto = ordem_no_alfabeto(letra)
    chave = pow(posicaoLetraAlfabeto, int(d), int(n))
    print("antes:", posicaoLetraAlfabeto)
    print("depois:", chave)
    return letra_no_alfabeto(chave)

def decript(texto):
    textoAlterado = ""
    for caract in texto:
        textoAlterado += trocaLetra(caract)
    return textoAlterado

def realizaLog(msg):
    if (geraLogsDebugs):
        print(msg)

clientSocket = socket(AF_INET, SOCK_STREAM)

print ("TCP Server em Execução")

abreSocket()
connectionSocket, addr = serverSocket.accept()

###################################

# Escolha aleatória de dois números primos grandes p e q
# p = number.getPrime(bitlen // 2, randfunc=number.getRandomRange)
# q = number.getPrime(bitlen // 2, randfunc=number.getRandomRange)

p = 3
q = 5

n = p * q

# função totiente
m = (p - 1) * (q - 1)

# Escolha de um inteiro "e", 1 < "e" < totiente, "e" e totiente devem ser primos entre si
e = m - 1
while number.GCD(m, e) > 1:
    e += 2

# d seja inverso multiplicativo de "e"
#d = number.inverse(e, m)
d = n
while True:
    if (e * d) % m == 1:
        break
    print(str(d))
    d -= 1

print("p:", p)
print("q:", q)
print("n:", n)
print("m:", m)
print("e:", e)
print("d:", d)

chave =  "(" + str(e) + "," + str(n) + ")"
print(chave)

###################################

enviaDado(chave)
time.sleep(1)
msgCript = connectionSocket.recv(65000)
msgCriptUnicode = str(msgCript,"utf-8")
msg = decript(msgCriptUnicode)
devolveMaiusculo = msg.upper()
#msgCriptoMaiusculo = criptDecript(devolveMaiusculo,K,False)
enviaDado(devolveMaiusculo)
realizaLog("Mensagem criptografada recebida: " + msgCriptUnicode)

print ("Mensagem decriptografada : ", msg)
print ("Mensagem devolvida para o client : ", devolveMaiusculo)


fechaSocket()