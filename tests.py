import unittest
import run
from PIL import Image, ImageDraw
import re

quote_lines = [
'My dream holiday would be a) a ticket to Amsterdam b) immunity from prosecution and c) a baseball bat  :-)',
'',
'        -- (Terry Pratchett, alt.fan.pratchett)'
]

long_multiline_quote = """
It's a sad and terrible thing that high-born folk really have thought that the servants would be totally fooled if spirits were put into decanters that were cunningly labelled *backwards*. 

And also throughout history the more politically conscious butler has taken it on trust, and with rather more justification, that his employers will not notice if the whisky is topped up with eniru.
        -- (Terry Pratchett, Hogfather)"""

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        # create new Image and draw the image
        img = Image.new('1', (400, 300), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(img)

        run.draw_pratchet_quote(long_multiline_quote, draw)

        #run.draw_pratchet_quote(run.get_pratchet_quote(randint(1,300)), draw)
        img.save('test.png')


    def test_re(self):
        text = '\n'.join(quote_lines)
        pair = re.split(r"\s+--", text)
        print(pair)

if __name__ == '__main__':
    unittest.main()
