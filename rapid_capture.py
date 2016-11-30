# -*- coding: utf-8 -*-

import io
import time
import threading
import picamera
import Image
import zbar

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []
scanner = zbar.ImageScanner()
scanner.parse_config('enable')

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    pil = Image.open(self.stream).convert('L')
	            width, height = pil.size
                    raw = pil.tostring()
                    image = zbar.Image(width, height, 'Y800', raw)
                    scanner.scan(image)
                    t = None
                    for symbol in image:
                        t = symbol
                        print('解码成功')
                    	print 'decodef', symbol.type, 'symbol', '''%s'''  % symbol.data
		    if not t:
                        print('解码失败或未扫描到二维码')

                    # Read the image and do some processing on it
                    #Image.open(self.stream)
                    #...
                    #...
                    # Set done to True if you want the script to terminate
                    # at some point
                    # done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)

with picamera.PiCamera() as camera:
    # ImageProcessor()类实例化的对象
    pool = [ImageProcessor() for i in range(4)]
    # 设置分辨率
    camera.resolution = (640, 480)
    # 设置帧数
    camera.framerate = 30
    camera.start_preview()
    time.sleep(2)
    # 捕获图像流
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
