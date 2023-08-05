'''
Generate a PDF of a pixel plane YAML file.

'''
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch
import yaml
from pixelplane import PixelPlane
import  numpy as np

with open('sensor_plane_28_simple.yaml', 'r') as f:
    pixelplane = PixelPlane.fromDict(yaml.load(f))

colors = np.array([[0, 174, 219], [162, 0, 255], [244, 120, 53], [212, 18, 67],
        [142, 193, 39]])/256.0



c = canvas.Canvas('sensor.pdf', pagesize=(12*inch, 12*inch))
c.setFont('Helvetica', 20)
c.drawString(4*inch, 11*inch, 'Sensor board with 4 chips')
c.drawString(4*inch, 10.6*inch, '(view from chip side)')
c.setFont('Courier', 7)
colorkey = []
for pixel in pixelplane.pixels.values():
    c.circle(pixel.x*7-300, 15*inch-pixel.y*7, 0.4)
    c.drawString(pixel.x*7-300 - 5, 15*inch-pixel.y*7, str(pixel.pixelid))
c.setFont('Courier', 9)
for chip, color in zip(pixelplane.chips.values(), colors):
    c.setFillColorRGB(*color)
    colorkey.append(['Chip %d' % chip.chipid, color])
    for channel, pixel in enumerate(chip.channel_connections):
        c.drawString(pixel.x*7-300 - 5, 15*inch-pixel.y*7-5, str(channel))
c.setFont('Helvetica', 16)
for i, (string, color) in enumerate(colorkey):
    c.setFillColorRGB(*color)
    c.drawString(80, 11*inch-25*i, string)
c.showPage()
c.save()
