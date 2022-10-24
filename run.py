#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

# picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image

from lib.waveshare_epd import waveshare_epd  
from lib.tcp_server import tcp_sver 
import socketserver
import logging

from progressbar import *

logging.basicConfig(level=logging.INFO)  

class MyServer(tcp_sver.tcp_sver):
    def handle(self):
        try:
            self.client = self.request
            logging.info('yo')
            #get id
            self.Get_ID()  
            #unlock if password = 123456
            self.unlock('123456')
            #init epd setting
            epd = waveshare_epd.EPD(4.2)
            #set image size
            self.set_size(epd.width,epd.height)
            #font 
            font24 = ImageFont.truetype(os.path.join(picdir, 'Font01.ttc'), 24)
            font18 = ImageFont.truetype(os.path.join(picdir, 'Font01.ttc'), 18)
            font35 = ImageFont.truetype(os.path.join(picdir, 'Font01.ttc'), 35)
            
            #creat new Image and draw the image
            Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)
            for x in range(0,10,9):
                draw.text((0, 0        +(x*20)), 'hello world', font = font24, fill = 0)
                draw.text((0, 20       +(x*20)), '2.13inch e-Paper', font = font18, fill = 0)
                draw.text((0, 40       +(x*20)), u'微雪电子', font = font18, fill = 0)    
                draw.line((20, 50       +(x*20), 70, 100     +(x*20)), fill = 0)
                draw.line((70, 50       +(x*20), 20, 100     +(x*20)), fill = 0)
                draw.rectangle((20, 50  +(x*20), 70, 100     +(x*20)), outline = 0)
                draw.line((165, 50      +(x*20), 165, 100    +(x*20)), fill = 0)
                draw.line((140, 75      +(x*20), 190, 75     +(x*20)), fill = 0)
                draw.arc((140, 50       +(x*20), 190, 100    +(x*20)), 0, 360, fill = 0)
                draw.rectangle((80, 50  +(x*20), 130, 100    +(x*20)), fill = 0)
                draw.chord((200, 50     +(x*20), 250, 100    +(x*20)), 0, 360, fill = 0) 
            #display
            self.flush_buffer(epd.getbuffer(Himage))
            #open image files
            #Himage = Image.open(os.path.join(picdir, '4in2.bmp'))
            #display
            #self.flush_buffer(epd.getbuffer(Himage))

            self.Send_cmd('S')                    
        except ConnectionResetError :
            self.Wait_write("lose connect.")
        except KeyboardInterrupt :
            self.close()
            os.system("clear")
        #except :
        #    pass
            
        
if __name__ == "__main__":
    ip=tcp_sver.get_host_ip()
    logging.info('{0}'.format(ip))
    socketserver.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((ip, 6868, ), MyServer)    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        os.system("clear")
    #except :
    #    pass
        
        


