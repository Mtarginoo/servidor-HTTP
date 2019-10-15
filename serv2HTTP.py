# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP (python 3)
#

# importacao das bibliotecas
import socket

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
print ('Serving HTTP on port %s ...' % PORT)

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    string = bytes.decode(request)
    
    try:
        x = string.split(' ')
        x2 = x[2].split('/')
        
        # declaracao da resposta do servidor

        if (x[0] == 'GET' and x2[0] == 'HTTP'):
            # imprime na tela o que o cliente enviou ao servidor    
            print (request.decode('utf-8'))
            if (x[1] == '/'):
                try:    
                    http_response = open('index.html').read()
                    http_response = """\HTTP/1.1 200 OK\r\n\r\n""" + http_response
                    
                except: 
                    http_response = open('notfound.html').read()
                    http_response = """\HTTP/1.1 404 Not Found\r\n\r\n""" + http_response
            else:
                try:
                    x3 = x[1].split('/')
                    http_response = open(x3[1]).read()
                    http_response = """\HTTP/1.1 200 OK\r\n\r\n""" + http_response
                except:
                    http_response = open('notfound.html').read()
                    http_response = """\HTTP/1.1 404 Not Found\r\n\r\n""" + http_response
        else:
            http_response = open('badrequest.html').read()
            http_response = """\HTTP/1.1 400 Bad Request\r\n\r\n""" + http_response
        # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
        client_connection.send(http_response.encode('utf-8'))
    except:
        http_response = open('badrequest.html').read()
        http_response = """\HTTP/1.1 400 Bad Request\r\n\r\n""" + http_response
        # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
        client_connection.send(http_response.encode('utf-8'))
    
    # encerra a conexao
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()