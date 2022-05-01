from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET,socket
import threading
from collections import deque
# ip_address = '42.193.138.254'
# server_port = 6222

# tcp_server = socket(AF_INET, SOCK_STREAM)

# tcp_server.bind((ip_address, server_port))

# tcp_server.listen(3)

# try:
#     while True:
#         conn, client_addr = tcp_server.accept()
#         try:
#             while True:
#                 recv = conn.recv(1024)
#                 if recv:
#                     print('客户端{0}:{1}'.format(client_addr, recv))
#         finally:
#             conn.close()
# finally:
#     tcp_server.close()

msg_dequeue = deque()

def dispose_client_request(tcp_client, client_address):
    #循环接受或发送数据
    while True:
        recv_data = tcp_client.recv(1024)

        #有消息就回复，消息长度为0即说明用户下线
        if recv_data:
            print('receve_data:', recv_data)
        #     pass
        # else:
        #     tcp_client.close()
        #     break

if __name__ == '__main__':
    IP_ADDRESS = '42.193.138.254'
    SERVER_PORT = 6222
    tcp_server = socket(AF_INET, SOCK_STREAM)
    #设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

    #绑定端口
    tcp_server.bind(('', SERVER_PORT))
    tcp_server.listen(4)

    #循环等待客户端链接
    while True:
        tcp_client1, client_address = tcp_server.accept()
        print('connect_client:', client_address)
        print(tcp_client1)
        #创建多线程对象
        thd = threading.Thread(target=dispose_client_request, args=(tcp_client1, client_address))

        #设置守护线程
        thd.setDaemon(True)

        #启动子线程
        thd.start()

