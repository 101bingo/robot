from socket import AF_INET, SOCK_STREAM, socket

ip_address = ''
server_port = 6222

tcp_server = socket(AF_INET, SOCK_STREAM)

tcp_server.bind((ip_address, server_port))

tcp_server.listen(3)

try:
    while True:
        conn, client_addr = tcp_server.accept()
        try:
            while True:
                recv = conn.recv(1024)
                if recv:
                    print('客户端{0}:{1}'.format(client_addr, recv))
        finally:
            conn.close()
finally:
    tcp_server.close()

