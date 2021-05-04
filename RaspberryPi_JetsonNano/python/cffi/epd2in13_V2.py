# *****************************************************************************
# * | File        :   epd2in13_V2.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V4.0
# * | Date        :   2019-06-20
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
from PIL import Image
from _DEV_Config_cffi import lib as libDEV
from _EPD_2in13_V2_cffi import ffi, lib as libEPD

class EPD_CFFI:
    def __init__(self, init=False):
        self.width = 122
        self.height = 250
        self.full_update = 0
        self.part_update = 1
        self.initialized = False

        if init:
            init(self.full_update)

    def __del__(self):
        if self.initialized:
            self.exit()

    def init(self, update):
        if libDEV.DEV_Module_Init() != 0:
            raise RuntimeError
        if update == self.full_update or update == self.part_update:
            libEPD.EPD_2IN13_V2_Init(update)
        else:
            raise ValueError("update must be either full_update ({self.full_update}) or part_update ({self.part_update})")
        self.initialized = True

    def to_cdata(self, buf):
        return ffi.from_buffer(buf)

    def getbuffer(self, image: Image) -> bytearray:
        '''converts a PIL.Image to bytearray'''
        img = image.convert('1').transpose(Image.FLIP_LEFT_RIGHT)
        img_width, img_height = img.size

        if img_width == self.height and img_height == self.width:
            img = img.rotate(270, expand=True)

        return bytearray(img.tobytes('raw'))

    def displayFromBytes(self, buf: bytearray):
        libEPD.EPD_2IN13_V2_Display(self.to_cdata(buf))

    def display(self, image: Image):
        '''image: PIL.Image'''
        self.displayFromBytes(self.getbuffer(image))

    def displayPartialFromBytes(self, buf: bytearray):
        libEPD.EPD_2IN13_V2_DisplayPart(self.to_cdata(buf))

    def displayPartial(self, image: Image):
        '''image: PIL.Image'''
        self.displayPartialFromBytes(self.getbuffer(image))

    def displayPartBaseImageFromBytes(self, buf: bytearray):
        libEPD.EPD_2IN13_V2_DisplayPartBaseImage(self.to_cdata(buf))

    def displayPartBaseImage(self, image: Image):
        '''image: PIL.Image'''
        self.displayPartBaseImageFromBytes(self.getbuffer(image))

    def reset(self):
        libEPD.EPD_2IN13_V2_Reset()

    def clear(self):
        libEPD.EPD_2IN13_V2_Clear()

    def sleep(self):
        libEPD.EPD_2IN13_V2_Sleep()

    def exit(self):
        self.sleep()
        libDEV.DEV_Module_Exit()
