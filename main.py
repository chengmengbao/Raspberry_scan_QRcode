# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# main.py


# import pic
import parse
import time


i = 0
while(1):
    
    main_t1 = time.time()

   # pic.take_pic(i)
    parse.lesen(i)

    i = i+1

    main_t2 = time.time()
    print "main_t2-main_t1=%f" % (main_t2-main_t1)

    print "#############################################"
