from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef('''
    void DEV_Digital_Write(uint16_t Pin, uint8_t Value);
    uint8_t DEV_Digital_Read(uint16_t Pin);

    void DEV_SPI_WriteByte(uint8_t Value);
    void DEV_SPI_Write_nByte(uint8_t *pData, uint32_t Len);
    void DEV_Delay_ms(uint32_t xms);

    uint8_t DEV_Module_Init(void);
    void DEV_Module_Exit(void);
''')

ffibuilder.set_source('_DEV_Config_cffi',
'''
     #include "../../c/lib/Config/DEV_Config.h"
''',
     libraries=['DEV_Config', 'wiringPi'],
     extra_link_args=['-L../../c/bin', '-L/lib'],
     extra_compile_args=['-I../../c/lib/Config'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
