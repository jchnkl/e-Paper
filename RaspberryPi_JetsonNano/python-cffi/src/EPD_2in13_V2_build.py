from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef('''
    void EPD_2IN13_V2_Init(uint8_t Mode);
    void EPD_2IN13_V2_Clear(void);
    void EPD_2IN13_V2_Display(uint8_t *Image);
    void EPD_2IN13_V2_DisplayPart(uint8_t *Image);
    void EPD_2IN13_V2_DisplayPartBaseImage(uint8_t *Image);
    void EPD_2IN13_V2_Sleep(void);
''')

ffibuilder.set_source('_EPD_2in13_V2_cffi',
'''
     #include "EPD_2in13_V2.h"
''',
     libraries=['EPD_2in13_V2', 'DEV_Config'], #, 'wiringPi'],
     extra_link_args=['-L../c/bin'],
     extra_compile_args=['-I../c/lib/Config', '-I../c/lib/e-Paper'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
