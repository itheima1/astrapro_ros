import socket
import struct
import time
import traceback

import cv2
import numpy


class Client(object):
    """客户端"""

    def __init__(self, addr_port=('172.16.0.200', 11000)):
        # 连接的服务器的地址
        # 连接的服务器的端口
        self.addr_port = addr_port
        # 创建套接字
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 地址端口可以复用
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 分辨率
        self.resolution = (640, 480)

    def connect(self):
        """链接服务器"""
        try:
            self.client.connect(self.addr_port)
            return True
        except Exception as e:
            traceback.print_exc()  # 打印原始的异常信息
            print('连接失败')
            return False

    def send2server(self):
        """读摄像头数据 发送给服务器"""
        camera = cv2.VideoCapture(0)  # 摄像头对象
        print('isOpened:', camera.isOpened())

        while camera.isOpened():

            try:
                # 获取摄像头数据
                ret, frame = camera.read()
                # 对每一帧图片做大小处理　和大小的压缩
                frame = cv2.resize(frame, self.resolution)
                # 参1图片后缀名 参2 原图片的数据 参3图片质量 0-100 越大越清晰
                ret, img = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
                # img 是被压缩后的数据 无法正常显示

                # 转换为numpy格式数据
                img_code = numpy.array(img)

                # 转为二进制数据
                img = img_code.tostring()

                # 获取数据长度
                length = len(img)

                # 发送的数据  大小 宽 高 图片数据

                # 数据打包变为二进制
                # pack方法参数1 指定打包数据的数据大小  i 4字节 h代表2字节
                all_data = struct.pack('ihh', length, self.resolution[0], self.resolution[1]) + img

                self.client.send(all_data)
                time.sleep(0.01)
            except:
                camera.release()  # 释放摄像头
                traceback.print_exc()
                return


if __name__ == '__main__':
    client = Client()
    if client.connect():
        client.send2server()


