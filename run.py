import os
import re
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

from d import DrawText, TextBlock, Align
from PIL import ImageDraw, ImageFont, Image
from random import randint
from lib.waveshare_epd import waveshare_epd  
from lib.tcp_server import tcp_sver 
import socketserver
import logging
from progressbar import *

logging.basicConfig(level=logging.INFO)  
font18 = ImageFont.truetype(os.path.join(picdir, 'Font01.ttc'), 18)

class ParsedQuote():
    def __init__(self, text):
        self.quote = re.split(r"\s+--", text)[0].strip()
        self.footer = re.split(r"\s+--", text)[1].strip()

    def draw_text_line(self, raw_text):
        return [DrawText(raw_text, font18)]

    def draw(self, image): 
        quote_wrapped_to_lines = text_wrap(self.quote, font18, image.im.size[0])
        quote_mapped_to_draw = list(map(self.draw_text_line, quote_wrapped_to_lines))

        footer_wrapped_to_lines = text_wrap(self.footer, font18, image.im.size[0])
        footer_mapped_to_draw = list(map(self.draw_text_line, footer_wrapped_to_lines))

        block1 = TextBlock(quote_mapped_to_draw, align=Align.Centre)
        block2 = TextBlock(footer_mapped_to_draw, align=Align.BottomLeft)
        block1.draw_on(image)
        block2.draw_on(image)

class WaveshareCloudQuoteServer(tcp_sver.tcp_sver):
    def handle(self):
        try:
            self.client = self.request
            #get id
            self.Get_ID()  
            #unlock if password = 123456
            self.unlock('123456')
            #init epd setting
            epd = waveshare_epd.EPD(4.2)
            #set image size
            self.set_size(epd.width, epd.height)
            
            #create new Image and draw the image
            Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)

            draw_pratchet_quote(get_pratchet_quote(randint(1,300)), draw)

            self.flush_buffer(epd.getbuffer(Himage))
            self.Send_cmd('S')                    
        except ConnectionResetError :
            self.Wait_write("lose connect.")
        except KeyboardInterrupt :
            self.close()
            os.system("clear")

def draw_pratchet_quote(quote, draw):
    text = ''.join(quote)
    parsed = ParsedQuote(text)
    parsed.draw(draw)

def get_pratchet_quote(target):
    empty_lines_count = 0
    quotes_read = 0
    quote = []
    with open('./pqf') as f:
        for line in f:
            if not line.strip():
                empty_lines_count += 1
            else:
                quote.append(line)
            if empty_lines_count == 2:
                quotes_read += 1
                empty_lines_count = 0
                if quotes_read == target:
                    break
                else:
                    quote.clear()
    return quote

def text_wrap(text, font = None, max_width = None):
    lines = []

    for split_line in text.split('\n'):
        if font.getlength(split_line) < max_width:
            lines.append(split_line)
        else:
            words = split_line.split(' ')
            word_count = 0
            while word_count < len(words):
                line = ''
                while word_count < len(words) and font.getlength(line + words[word_count]) <= max_width:
                    line = line + words[word_count] + " "
                    word_count += 1
                if not line:
                    line = words[word_count]
                    word_count += 1
                lines.append(line)
    return lines
        
if __name__ == "__main__":
    ip=tcp_sver.get_host_ip()
    logging.info('{0}'.format(ip))
    socketserver.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((ip, 6868, ), WaveshareCloudQuoteServer)    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        os.system("clear")
    except :
       pass
        
        


