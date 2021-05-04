#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys
import time
import logging
import argparse
from PIL import Image,ImageDraw,ImageFont

from epd2in13_V2 import EPD_CFFI as EPD

logging.basicConfig(level=logging.DEBUG)

__parser = argparse.ArgumentParser()
__basename = os.path.dirname(os.path.realpath(__file__))
__parser.add_argument('--picdir', default=os.path.join(__basename, 'pic'))
__parser.add_argument('--libdir', default=os.path.join(__basename, 'lib'))
__args = __parser.parse_args()

picdir = __args.picdir
libdir = __args.libdir

if os.path.exists(libdir):
    sys.path.append(libdir)


try:
    epd = EPD()

    logging.info("init and clear")
    epd.init(epd.full_update)
    epd.clear()

    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    if False:
        logging.info("1.Drawing on the image...")
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        draw.rectangle([(0,0),(50,50)],outline = 0)
        draw.rectangle([(55,0),(100,50)],fill = 0)
        draw.line([(0,0),(50,50)], fill = 0,width = 1)
        draw.line([(0,50),(50,0)], fill = 0,width = 1)
        draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
        draw.ellipse((55, 60, 95, 100), outline = 0)
        draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
        draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
        draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
        draw.polygon([(190,0),(190,50),(150,25)],fill = 0)
        draw.text((120, 60), 'e-Paper demo', font = font15, fill = 0)
        draw.text((110, 90), u'微雪电子', font = font24, fill = 0)
        epd.display(image)
        time.sleep(2)

    if False:
        # read bmp file
        logging.info("2.read bmp file...")
        image = Image.open(os.path.join(picdir, '2in13.bmp'))
        epd.display(image)
        logging.info("2.sleeping...")
        epd.sleep()
        time.sleep(2)

    if False:
        # read bmp file on window
        logging.info("3.read bmp file on window...")
        # epd.clear(0xFF)
        image1 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
        image1.paste(bmp, (2,2))
        epd.display(image1)
        time.sleep(2)

    if True:
        # # partial update
        logging.info("4.show time...")
        time_image = Image.new('1', (epd.height, epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)

        epd.init(epd.full_update)
        epd.displayPartBaseImage(time_image)

        epd.init(epd.part_update)
        num = 0
        while (True):
            text = time.strftime('%H:%M:%S')
            time_draw.rectangle((10, 10, 220, 105), fill = 255)
            time_draw.text((10, 10), text, font = font24, fill = 0)
            start = time.time()
            epd.displayPartial(time_image)
            stop = time.time()
            print(f'{text} :: displayPartial took {stop - start}')
            num = num + 1
            if(num == 30):
                break
        # epd.clear(0xFF)
        logging.info("clear...")
        epd.init(epd.full_update)
        epd.clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    epd.exit()

except Exception as e:
    logging.info(e)
    epd.clear()
    epd.exit()

except BaseException as e:
    logging.info(e)
    epd.clear()
    epd.exit()
