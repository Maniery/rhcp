import sys
from rhcp import getRHCP, find_version, IRHCP

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

def receive_request(client):
    '''
    Lê cada linha da requisição e retorna essas linhas formatadas em uma string.

    Interrompe o loop quando não receber resposta ou estiver numa linha em branco.
    '''
    data = []
    while True:
        msq_req = client.recv(4096).decode()
        if not msq_req:
            break
        data.append(msq_req)
        if "\r\n" == msq_req:
            break
    return ''.join(data)

while True:
    # espera por uma conexao
    (clientsocket, clientaddress) = s.accept()

    print(f"Uma conexao com o endereco {clientaddress[0]}:{clientaddress[1]} foi estabelecida")

    # obtendo a mensagem de requisicao
    msg_req = ''
    try:
        msg_req = receive_request(clientsocket)
    except:
        clientsocket.send(f'RHCP/1.0 500 Internal Server Error\r\n\r\n'.encode())
        continue
    # print(f"REQUISICAO: {msg_req}")

    # TODO:
    # - processar a mensagem no formato adequado
    # - carregar os dados do arquivo status.csv
    # - alterar o valor solicitado
    # - salvar o valor alterado no arquivo csv
    # - retornar uma mensagem de resposta ao cliente

    # enviando a mensagem de resposta ao cliente
    rhcp: IRHCP = getRHCP(find_version(msg_req))
    if rhcp is not None:
        rhcp.format_request(msg_req)
        msg_res = rhcp.process().encode()
    else:
        msg_res = f'RHCP/1.0 500 Internal Server Error\r\n\r\n'.encode()

    clientsocket.send(msg_res)

    # finalizando o socket do cliente
    clientsocket.close()
