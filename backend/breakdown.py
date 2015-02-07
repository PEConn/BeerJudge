from PIL import Image, ImageDraw, ImageFont
import math

class Breakdown:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.flavours = ['greeny_hoppy', 'roasted_toasted', 'citrus_zesty', 
                         'sour', 'spicey', 'fruity', 'toffee_caramel']
        self.colours = [(242, 108, 79), (251, 175, 93), (124, 197, 118), (0, 191, 243),
                        (86, 116, 185), (133, 96, 168), (240, 110, 170),
                        (158, 11, 15), (136, 98, 10), (25, 123, 48), (0, 118, 163),
                        (0, 52, 1113), (68, 14, 98), (158, 0, 93)]
        self.total = len(self.flavours) * 2
        self.base = 0.4

    def drawSegment(self, draw, value, no, col):
        f = 360.0/self.total
        x = self.width / 2.0
        y = self.height / 2.0
        r = self.base*x + value * (x - x*self.base)

        offset = f / 2

        draw.pieslice([x-r, y-r, x+r, y+r], int(no*f + offset), int((no+1)*f + offset), fill=col)

    def drawTitle(self, draw, text):
        x = self.width / 2.0
        y = self.height / 2.0
        r = self.base * x

        draw.pieslice([x-r, y-r, x+r, y+r], 0, 360, (180, 180, 180))
        # font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=20)
        # fs = draw.textsize(text);
        # draw.text([(self.width - fs[0])/2, (self.height - fs[1]/2)], text, fill=(0,0,0), font=font)
        
    def drawBreakdown(self, name, bd):
        img = Image.new("RGB", (self.width, self.height), "white")
        draw = ImageDraw.Draw(img)
        cons = bd[0]
        acc = bd[1]

        largest = 0
        for (i, f) in enumerate(self.flavours):
            if f in acc:
                largest = max(acc[f], largest)
            if f in cons:
                largest = max(cons[f], largest)
        largest = math.sqrt(largest)

        for (i, f) in enumerate(self.flavours):
            if f in acc:
                self.drawSegment(draw, math.sqrt(acc[f]) / largest, i, self.colours[i])
            if f in cons:
                offset = len(self.flavours)
                self.drawSegment(draw, math.sqrt(cons[f]) / largest, i + offset, self.colours[i + offset])

        self.drawTitle(draw, name)

        del draw
        return img
            

f = ({u'spicy': 1, u'citrus_zesty': 33}, {u'citrus_zesty': 4, u'spicy': 2, u'roasted_toasted': 13, u'fruity': 14, u'toffee_caramel': 1})
bd = Breakdown(2048, 2048)
big = bd.drawBreakdown('chicken', f)
big.thumbnail([512, 512], Image.ANTIALIAS)
big.show()
