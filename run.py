#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from queue import Empty
import sys

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image

from lib.waveshare_epd import waveshare_epd  
from lib.tcp_server import tcp_sver 
import socketserver
import logging
font24 = ImageFont.truetype(os.path.join(picdir, 'Font01.ttc'), 24)

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

            quote = get_pratchet_quote(1)
            
            for idx, x in enumerate(quote):
                draw.text((0, idx * 15), x, font = font24, fill = 0)

            self.flush_buffer(epd.getbuffer(Himage))
            self.Send_cmd('S')                    
        except ConnectionResetError :
            self.Wait_write("lose connect.")
        except KeyboardInterrupt :
            self.close()
            os.system("clear")

def get_pratchet_quote():
    steps = 0
    quotes_read = 0
    target = 1
    quote = []
    with open('./pqf') as f:
        for line in f:
            if not line.strip():
                steps += 1
            else:
                quote.add(line)
            if steps == 2:
                quotes_read += 1
                steps = 0
            if quotes_read == target:
                break

    return quote
            
        
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
        
        


