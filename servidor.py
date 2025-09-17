import sys

# importando o modulo socket
import socket

# verificando os argumentos passados
if len(sys.argv) == 2:
    # definindo a porta do servidor
    # obtendo o valor da porta da linha de comando
    PORTA_SERVIDOR_RHCP = int(sys.argv[1])
    print(f"Hello, !")
else:
    print("Erro, informe a PORTA do servidor")
    exit(1)

# definindo o IP do servidor / em branco para obter automaticamente e permitir
# acesso de qualuer iP de origem
IP = ""

# criando um socket Internet (INET IPv4) sobre TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# liga o socket ao enderecamento do servidor
s.bind((IP, PORTA_SERVIDOR_RHCP))

# habilita a escuta de conexoes
s.listen(1)

print(f"Servidor RHCP na porta TCP: {PORTA_SERVIDOR_RHCP}")

while True:
    # espera por uma conexao
    (clientsocket, clientaddress) = s.accept()

    print(f"Uma conexao com o endereco {clientaddress[0]}:{clientaddress[1]} foi estabelecida")

    # obtendo a mensagem de requisicao
    msg_req = clientsocket.recv(4096).decode()
    print(f"REQUISICAO: {msg_req}")

    # TODO:
    # - processar a mensagem no formato adequado
    # - carregar os dados do arquivo status.csv
    # - alterar o valor solicitado
    # - salvar o valor alterado no arquivo csv
    # - retornar uma mensagem de resposta ao cliente

    # enviando a mensagem de resposta ao cliente
    msg_res = "MENSAGEM DE RESPOSTA AQUI".encode()
    clientsocket.send(msg_res)

    # finalizando o socket do cliente
    clientsocket.close()
