# importando o modulo socket
import socket

# definindo o IP do servidor
IP_SERVIDOR_RHCP = "127.0.0.1"

# definindo a porta do servidor
PORTA_SERVIDOR_RHCP = 8000

# criando um socket Internet (INET IPv4) sobre TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conectando ao servidor
s.connect((IP_SERVIDOR_RHCP, PORTA_SERVIDOR_RHCP))

# enviando a requisicao
msg_req = "MENSAGEM DE REQUISICAO AQUI".encode()
s.send(msg_req)

# recebendo a resposta
msg_res = s.recv(500)
# tratando a resposta
print(f"RESPOSTA: {msg_res}")

# fechando o socket
s.close()
