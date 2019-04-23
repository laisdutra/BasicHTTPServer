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

def abre_pagina(pagina):
    f = open(pagina, 'r')
    conteudo = f.read()
    f.close()

    return conteudo

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    print request
    # quebra os dados recebidos em um vetor
    request_vector = request.split()
    
    caminho = request_vector[1]
    
    # verifica o protocolo HTTP
    if request_vector[0] == 'GET' and caminho[0] == '/' and request_vector[2] == 'HTTP/1.1':
        # testa existencia da página
        if os.path.isfile(caminho[1:]):
            http_response =  "HTTP/1.1 200 OK\r\n\r\n" + abre_pagina(caminho[1:])
            
        elif caminho == '/':
            http_response =  "HTTP/1.1 200 OK\r\n\r\n" + abre_pagina('index.html')

        else:
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n" + abre_pagina('404.html')

    # se não atende ao protocolo
    else:
        http_response = "HTTP/1.1 400 Bad Request\r\n\r\n" + abre_pagina('400.html')

    # servidor retorna o que foi solicitado pelo cliente
    client_connection.send(http_response)
    
    # encerra a conexão
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()
