# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# parse.py

import zbar
import Image
import os
import io
import picamera
import StringIO
import time 


camera = picamera.PiCamera()
camera.resolution = (360, 240)
camera.start_preview()
# 解二维码
def lesen(i):
	parse_t0 = time.time()

	# create a reader
	scanner = zbar.ImageScanner()

	# configure the reader
	scanner.parse_config('enable')

	# obtain image data
	# pil = Image.open("/home/pi/camera_zbarcode/pic%d.jpg" % i).convert('L')

        parse_t1 = time.time()
        print "parse_t1-parse_t0=%f" % (parse_t1-parse_t0)

	my_stream = io.BytesIO()
	#my_stream = StringIO.StringIO()
        camera.capture(my_stream, 'jpeg')
	
        parse_t2 = time.time()
        print "parse_t2-parse_t1=%f" % (parse_t2 - parse_t1)
	
        pil = Image.open(io.BytesIO(my_stream.getvalue())).convert('L')
	width, height = pil.size
        print(width, height)
	raw = pil.tostring()
	
        parse_t3 = time.time()	
	print "parse_t3-parse_t2=%f" % (parse_t3 - parse_t2)

	# wrap image data
	image = zbar.Image(width, height, 'Y800', raw)

	# scan the image for barcodes
	scanner.scan(image)

	parse_t4 = time.time()
	print "parse_t4-parse_t3=%f" % (parse_t4 - parse_t3)
	# wrap image data

	# extract results
        t = None
	for symbol in image: 
		t = symbol
		print "解码成功"
		# do something useful with results
		print 'decodef', symbol.type, 'symbol', '''%s'''  % symbol.data
	if not t:	
		print "解码不成功或未扫描到二维码"
               # os.remove("pic%d.jpg" % i)
	else:				
	#	os.rename("pic%d.jpg" % i, "pic_success%d.jpg" % i)
		pass
	# clean up
	del(image)
