from skidl import Pin, Part, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

video = SchLib(tool=SKIDL).add_parts(*[
        Part(name='AD725',dest=TEMPLATE,tool=SKIDL,keywords='Video',description='Low Cost RGB to NTSC/PAL Encoder with Luma Trap Port',ref_prefix='U',num_units=1,fplist=['SOIC*7.5x10.3mm*Pitch1.27mm*'],do_erc=True,pins=[
            Pin(num='1',name='NTSC/PAL',do_erc=True),
            Pin(num='2',name='AGND',func=Pin.PWRIN,do_erc=True),
            Pin(num='3',name='4FSC_CLK',do_erc=True),
            Pin(num='4',name='AVCC',func=Pin.PWRIN,do_erc=True),
            Pin(num='5',name='CE',func=Pin.PWRIN,do_erc=True),
            Pin(num='6',name='RED',do_erc=True),
            Pin(num='7',name='GREEN',do_erc=True),
            Pin(num='8',name='BLUE',do_erc=True),
            Pin(num='9',name='CHROM_OUT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='10',name='CVBS_OUT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='11',name='LUM_OUT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='12',name='TRAP',do_erc=True),
            Pin(num='13',name='DGND',func=Pin.PWRIN,do_erc=True),
            Pin(num='14',name='DVCC',func=Pin.PWRIN,do_erc=True),
            Pin(num='15',name='VSYNC',do_erc=True),
            Pin(num='16',name='HSYNC',do_erc=True)]),
        Part(name='AD9891',dest=TEMPLATE,tool=SKIDL,keywords='CCD Signal Processor',description='CCD Signal Processor, 20MHz 10bits, CSPBGA-64',ref_prefix='U',num_units=1,fplist=['BGA*10x10*9.0x9.0mm*Pitch0.8mm*'],do_erc=True,pins=[
            Pin(num='A1',name='VD',func=Pin.BIDIR,do_erc=True),
            Pin(num='B1',name='HD',func=Pin.BIDIR,do_erc=True),
            Pin(num='C1',name='SYNC',do_erc=True),
            Pin(num='D1',name='DCLK',func=Pin.OUTPUT,do_erc=True),
            Pin(num='F1',name='D1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='G1',name='D3',func=Pin.OUTPUT,do_erc=True),
            Pin(num='H1',name='D5',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J1',name='D7',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K1',name='D9',do_erc=True),
            Pin(num='A2',name='DVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='B2',name='DVSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='C2',name='LD/FD',func=Pin.OUTPUT,do_erc=True),
            Pin(num='D2',name='PBLK/CLPOB',func=Pin.OUTPUT,do_erc=True),
            Pin(num='F2',name='D0/SD0',func=Pin.OUTPUT,do_erc=True),
            Pin(num='G2',name='D2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='H2',name='D4',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J2',name='D6',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K2',name='D8',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A3',name='MSHUT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B3',name='STROBE',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J3',name='VSUB',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K3',name='DRVDD',func=Pin.PWROUT,do_erc=True),
            Pin(num='A4',name='SDI',do_erc=True),
            Pin(num='B4',name='SCK',do_erc=True),
            Pin(num='J4',name='SUBCK',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K4',name='DRVSS',func=Pin.PWROUT,do_erc=True),
            Pin(num='A5',name='REFT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B5',name='SL',do_erc=True),
            Pin(num='J5',name='V2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K5',name='V1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A6',name='REFB',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B6',name='AVSS2',func=Pin.PWRIN,do_erc=True),
            Pin(num='J6',name='V4',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K6',name='V3',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A7',name='BYP3',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B7',name='AVDD2',func=Pin.PWRIN,do_erc=True),
            Pin(num='J7',name='VSG2/V6',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K7',name='VSG1/V5',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A8',name='CDD-IN',do_erc=True),
            Pin(num='B8',name='BYP2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J8',name='VSG4/V8',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K8',name='VSG3/V7',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A9',name='BYP1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B9',name='AVSS1',func=Pin.PWRIN,do_erc=True),
            Pin(num='C9',name='TCVSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='D9',name='RG',func=Pin.OUTPUT,do_erc=True),
            Pin(num='E9',name='RGVSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='F9',name='H4',func=Pin.OUTPUT,do_erc=True),
            Pin(num='G9',name='HVSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='H9',name='H2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J9',name='VSG6',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K9',name='VSG5',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A10',name='AVDD1',func=Pin.PWRIN,do_erc=True),
            Pin(num='B10',name='TCVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='C10',name='CLI',do_erc=True),
            Pin(num='D10',name='CLO',func=Pin.OUTPUT,do_erc=True),
            Pin(num='E10',name='RGVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='F10',name='H3',func=Pin.OUTPUT,do_erc=True),
            Pin(num='G10',name='HVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='H10',name='H1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J10',name='VSG8',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K10',name='VSG7',func=Pin.OUTPUT,do_erc=True)]),
        Part(name='AD9895',dest=TEMPLATE,tool=SKIDL,keywords='CCD Signal Processor',description='CCD Signal Processor, 30MHz 12bits, CSPBGA-64',ref_prefix='U',num_units=1,fplist=['BGA*10x10*9.0x9.0mm*Pitch0.8mm*'],do_erc=True,pins=[
            Pin(num='A1',name='VD',func=Pin.BIDIR,do_erc=True),
            Pin(num='B1',name='HD',func=Pin.BIDIR,do_erc=True),
            Pin(num='C1',name='SYNC',do_erc=True),
            Pin(num='D1',name='DCLK',func=Pin.OUTPUT,do_erc=True),
            Pin(num='E1',name='D1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='F1',name='D3',func=Pin.OUTPUT,do_erc=True),
            Pin(num='G1',name='D5',func=Pin.OUTPUT,do_erc=True),
            Pin(num='H1',name='D7',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J1',name='D9',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K1',name='D11',do_erc=True),
            Pin(num='A2',name='DVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='B2',name='DVSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='C2',name='LD/FD',func=Pin.OUTPUT,do_erc=True),
            Pin(num='D2',name='PBLK/CLPOB',func=Pin.OUTPUT,do_erc=True),
            Pin(num='E2',name='D0',func=Pin.OUTPUT,do_erc=True),
            Pin(num='F2',name='D2/SD0',func=Pin.OUTPUT,do_erc=True),
            Pin(num='G2',name='D4',func=Pin.OUTPUT,do_erc=True),
            Pin(num='H2',name='D6',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J2',name='D8',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K2',name='D10',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A3',name='MSHUT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B3',name='STROBE',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J3',name='VSUB',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K3',name='DRVDD',func=Pin.PWROUT,do_erc=True),
            Pin(num='A4',name='SDI',do_erc=True),
            Pin(num='B4',name='SCK',do_erc=True),
            Pin(num='J4',name='SUBCK',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K4',name='DRVSS',func=Pin.PWROUT,do_erc=True),
            Pin(num='A5',name='REFT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B5',name='SL',do_erc=True),
            Pin(num='J5',name='V2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K5',name='V1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A6',name='REFB',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B6',name='AVSS2',func=Pin.PWRIN,do_erc=True),
            Pin(num='J6',name='V4',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K6',name='V3',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A7',name='BYP3',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B7',name='AVDD2',func=Pin.PWRIN,do_erc=True),
            Pin(num='J7',name='VSG2/V6',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K7',name='VSG1/V5',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A8',name='CDD-IN',do_erc=True),
            Pin(num='B8',name='BYP2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J8',name='VSG4/V8',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K8',name='VSG3/V7',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A9',name='BYP1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='B9',name='AVSS1',func=Pin.PWRIN,do_erc=True),
            Pin(num='C9',name='TCVSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='D9',name='RG',func=Pin.OUTPUT,do_erc=True),
            Pin(num='E9',name='RGVSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='F9',name='H4',func=Pin.OUTPUT,do_erc=True),
            Pin(num='G9',name='HVSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='H9',name='H2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J9',name='VSG6',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K9',name='VSG5',func=Pin.OUTPUT,do_erc=True),
            Pin(num='A10',name='AVDD1',func=Pin.PWRIN,do_erc=True),
            Pin(num='B10',name='TCVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='C10',name='CLI',do_erc=True),
            Pin(num='D10',name='CLO',func=Pin.OUTPUT,do_erc=True),
            Pin(num='E10',name='RGVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='F10',name='H3',func=Pin.OUTPUT,do_erc=True),
            Pin(num='G10',name='HVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='H10',name='H1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J10',name='VSG8',func=Pin.OUTPUT,do_erc=True),
            Pin(num='K10',name='VSG7',func=Pin.OUTPUT,do_erc=True)]),
        Part(name='AV9173',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='CX7930',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='CXD3400N',dest=TEMPLATE,tool=SKIDL,keywords='CCD Clock Driver',description='6-channel Vertical Clock Driver for CCD Image Sensor, SSOP-20',ref_prefix='U',num_units=1,fplist=['SSOP*'],do_erc=True,pins=[
            Pin(num='1',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='2',name='XSHT',do_erc=True),
            Pin(num='3',name='XV3',do_erc=True),
            Pin(num='4',name='XSG3B',do_erc=True),
            Pin(num='5',name='XSG3A',do_erc=True),
            Pin(num='6',name='XV1',do_erc=True),
            Pin(num='7',name='XSG1B',do_erc=True),
            Pin(num='8',name='XSG1A',do_erc=True),
            Pin(num='9',name='XV4',do_erc=True),
            Pin(num='10',name='XV2',do_erc=True),
            Pin(num='20',name='SHT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='11',name='GND',func=Pin.PWRIN,do_erc=True),
            Pin(num='12',name='V2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='13',name='V4',func=Pin.OUTPUT,do_erc=True),
            Pin(num='14',name='V1A',func=Pin.OUTPUT,do_erc=True),
            Pin(num='15',name='VH',func=Pin.PWRIN,do_erc=True),
            Pin(num='16',name='V1B',func=Pin.OUTPUT,do_erc=True),
            Pin(num='17',name='V3A',func=Pin.OUTPUT,do_erc=True),
            Pin(num='18',name='VL',func=Pin.PWRIN,do_erc=True),
            Pin(num='19',name='V3B',func=Pin.OUTPUT,do_erc=True)]),
        Part(name='HD63484',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='HD63484_PLCC',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='ICX415AQ',dest=TEMPLATE,tool=SKIDL,keywords='CCD B/W Image Sensor',description='Diagonal 8mm B/W Progressive Scan CCD Image Sensor with Square Pixel, CERDIP-22',ref_prefix='U',num_units=1,do_erc=True,pins=[
            Pin(num='3',name='V3',do_erc=True),
            Pin(num='4',name='V2',do_erc=True),
            Pin(num='5',name='V1',do_erc=True),
            Pin(num='7',name='GND',func=Pin.PWRIN,do_erc=True),
            Pin(num='9',name='VOUT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='10',name='CGG',do_erc=True),
            Pin(num='20',name='CSUB',do_erc=True),
            Pin(num='21',name='SUBCIR',func=Pin.PWRIN,do_erc=True),
            Pin(num='12',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='13',name='RG',do_erc=True),
            Pin(num='14',name='VL',func=Pin.PWRIN,do_erc=True),
            Pin(num='15',name='SUB',do_erc=True),
            Pin(num='16',name='H1',do_erc=True),
            Pin(num='17',name='H2',do_erc=True)]),
        Part(name='LM1881',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='MAX310',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='MAX311',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='MB88303P',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='S178',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='SI582',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='TDA1950',dest=TEMPLATE,tool=SKIDL,do_erc=True,aliases=['TDA1950F']),
        Part(name='TDA2593',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='TDA7260',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='TDA9500',dest=TEMPLATE,tool=SKIDL,do_erc=True,aliases=['TDA9503', 'TDA9513']),
        Part(name='TEA5115',dest=TEMPLATE,tool=SKIDL,do_erc=True)])