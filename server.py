import socket
import struct
import threading
import cv2
import numpy


class Server:
    def __init__(self):
        # 设置tcp服务端的socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置重复使用
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定地址和端口
        self.server.bind(('0.0.0.0', 11000))
        # 设置被动监听
        self.server.listen(128)

    def run(self):
        while True:
            print('等待客户端连接')
            # 等待客户端连接
            client, addr = self.server.accept()
            ProcessClient(client).start()


class ProcessClient(threading.Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while True:
            data = self.client.recv(8)
            if not data:
                break
            # 图片的长度 图片的宽高
            length, width, height = struct.unpack('ihh', data)

            imgg = b''  # 存放最终的图片数据
            while length:
                # 接收图片
                temp_size = self.client.recv(length)
                length -= len(temp_size)  # 每次减去收到的数据大小
                imgg += temp_size  # 每次收到的数据存到img里

            # 把二进制数据还原
            data = numpy.frombuffer(imgg, dtype='uint8')
 
            # 还原成矩阵数据
            image = data.reshape(height,width,3)
          
            cv2.imshow('窗口1', image)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    server = Server()
    server.run()

