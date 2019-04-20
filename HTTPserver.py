# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP
#

# importacao das bibliotecas
import socket
import os

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print 'Servidor HTTP aguardando conexoes na porta %s ...' % PORT


# aguarda por novas conexoes
client_connection, client_address = listen_socket.accept()
while True:
  
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    print request
    #quebra os dados recebidos em um vetor
    request_vector = request.split()
    #tamanho do vetor
    tamanho = len(request_vector)
    if tamanho > 1:
        #caso o tenha espa�o no nome do arquivo
        if request_vector[1][:5] != '.html':
            nome_arquivo = ""
            for i in range(1, tamanho-1):
                nome_arquivo += request_vector[i] + ' '
            nome_arquivo = nome_arquivo[:-1]
        else:
            nome_arquivo = request_vector[1]
    #checa se mandou GET e o protocolo
    if (request_vector[0] == 'GET') and (request_vector[tamanho-1] == 'HTTP/1.1') :
    #checa se o arquivo existe
        if os.path.isfile(nome_arquivo[1:]):
            http_response =  "HTTP/1.1 200 OK\r\n\r\n"
            #abre o arquivo para leitura
            arquivo = open(nome_arquivo[1:], 'r')
            #l� o arquivo
            conteudo = arquivo.read()
            arquivo.close()
            client_connection.send(http_response)
            client_connection.send(str(conteudo))
            #encerra a conexao
            client_connection.close()
        elif request_vector[1] == '/':
            http_response =  "HTTP/1.1 200 OK\r\n\r\n"
            arquivo = open('index.html', 'r')
            #l� o arquivo
            conteudo = arquivo.read()
            arquivo.close()
            client_connection.send(http_response)
            client_connection.send(str(conteudo))
            #encerra a conexao
            client_connection.close()
        else:
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conteudo = """\
    <html>
        <head></head>
        <body>
            <h1>404 Not Found</h1>
        </body>
    </html>\r\n
"""
            client_connection.send(http_response)
            client_connection.send(conteudo)
    #se nao for GET ou n�o atende ao protocolo
    else:
        http_response = "HTTP/1.1 400 Bad Request\r\n\r\n"
        conteudo = """\
    <html>
        <head></head>
        <body>
            <h1>400 Bad Resquest</h1>
        </body>
    </html>\r\n
"""
    client_connection.send(http_response)
    client_connection.send(conteudo)

# encerra o socket do servidor
listen_socket.close()
