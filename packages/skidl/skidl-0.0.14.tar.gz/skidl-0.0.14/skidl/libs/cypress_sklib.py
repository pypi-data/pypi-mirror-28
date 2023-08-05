from skidl import Pin, Part, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

cypress = SchLib(tool=SKIDL).add_parts(*[
        Part(name='CY7C185',dest=TEMPLATE,tool=SKIDL,do_erc=True,aliases=['CY7C186']),
        Part(name='CY7C194',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='CY7C199',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='CY7C261',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='CY7C263',dest=TEMPLATE,tool=SKIDL,do_erc=True,aliases=['CY7C264']),
        Part(name='CY7C271',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name='CY7C420',dest=TEMPLATE,tool=SKIDL,do_erc=True,aliases=['CY7C421', 'CY7C424', 'CY7C425', 'CY7C428', 'CY7C429']),
        Part(name='CY8C4xx7LQI-4xx',dest=TEMPLATE,tool=SKIDL,keywords='CYPRESS PSOC BLE CY8 CY8C4 ARM CORTEX M0 BLUETOOTH QFN',description='Programmable System-on-Chip With Bluetooth Low Energy, 24/48-MHz ARM® Cortex®-M0 , 56-QFN',ref_prefix='U',num_units=1,fplist=['QFN-56-1EP'],do_erc=True,aliases=['CY8C4127LQI-BL473', 'CY8C4127LQI-BL453', 'CY8C4127LQI-BL483', 'CY8C4127LQI-BL493', 'CY8C4247LQI-BL473', 'CY8C4247LQI-BL453', 'CY8C4247LQI-BL463', 'CY8C4247LQI-BL483', 'CY8C4247LQI-BL493', 'CY8C4247LQQ-BL483'],pins=[
            Pin(num='1',name='VDDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='2',name='XTAL32O/P6.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='3',name='XTAL32I/P6.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='4',name='XRES',do_erc=True),
            Pin(num='5',name='P4.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='6',name='P4.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='7',name='P5.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='8',name='P5.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='9',name='VSSD',func=Pin.PWRIN,do_erc=True),
            Pin(num='10',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='20',name='P0.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='30',name='P1.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='40',name='P2.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='50',name='P3.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='11',name='GANT1',func=Pin.PWRIN,do_erc=True),
            Pin(num='21',name='P0.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='31',name='P1.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='41',name='P2.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='51',name='P3.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='12',name='ANT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='22',name='P0.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='32',name='P1.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='42',name='P2.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='52',name='P3.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='13',name='GANT2',func=Pin.PWRIN,do_erc=True),
            Pin(num='23',name='VDDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='33',name='P1.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='43',name='P2.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='53',name='P3.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='14',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='24',name='P0.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='34',name='P1.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='44',name='P2.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='54',name='P3.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='15',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='25',name='P0.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='35',name='P1.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='45',name='VREF',func=Pin.PASSIVE,do_erc=True),
            Pin(num='55',name='VSSA',func=Pin.PWRIN,do_erc=True),
            Pin(num='16',name='XTAL24I',do_erc=True),
            Pin(num='26',name='P0.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='36',name='VDDA',func=Pin.PWRIN,do_erc=True),
            Pin(num='46',name='VDDA',func=Pin.PWRIN,do_erc=True),
            Pin(num='56',name='VCCD',func=Pin.PWROUT,do_erc=True),
            Pin(num='17',name='XTAL24O',func=Pin.OUTPUT,do_erc=True),
            Pin(num='27',name='P0.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='37',name='P2.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='47',name='P3.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='57',name='GND_EP',func=Pin.PWRIN,do_erc=True),
            Pin(num='18',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='28',name='P1.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='38',name='P2.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='48',name='P3.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='19',name='P0.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='29',name='P1.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='39',name='P2.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='49',name='P3.2',func=Pin.BIDIR,do_erc=True)]),
        Part(name='CY8CMBR3002',dest=TEMPLATE,tool=SKIDL,keywords='Touch Sensor 2ch',description='CapSense Controller, 2 Sensors, SOIC-8',ref_prefix='U',num_units=1,fplist=['SOIC-8*'],do_erc=True,pins=[
            Pin(num='1',name='GPO1',func=Pin.OUTPUT,do_erc=True),
            Pin(num='2',name='CMOD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='VCC',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='5',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='6',name='CS1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='7',name='CS0',func=Pin.PASSIVE,do_erc=True),
            Pin(num='8',name='GPO0',func=Pin.OUTPUT,do_erc=True)]),
        Part(name='CY8CMBR3102',dest=TEMPLATE,tool=SKIDL,keywords='Touch Sensor 2ch',description='CapSense Controller, 2 Sensors, SOIC-8',ref_prefix='U',num_units=1,fplist=['SOIC-8*'],do_erc=True,pins=[
            Pin(num='1',name='SCL',do_erc=True),
            Pin(num='2',name='CMOD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='VCC',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='5',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='6',name='CS1/PS1/GPO0/SH',func=Pin.BIDIR,do_erc=True),
            Pin(num='7',name='CS0/PS0',func=Pin.PASSIVE,do_erc=True),
            Pin(num='8',name='SDA',func=Pin.BIDIR,do_erc=True)]),
        Part(name='CY8CMBR3106S',dest=TEMPLATE,tool=SKIDL,keywords='Touch Sensor 16ch Slider',description='CapSense Controller, 16 Sensors w/ Slider, QFN-24+EP',ref_prefix='U',num_units=1,fplist=['QFN-24*'],do_erc=True,pins=[
            Pin(num='1',name='CS0/PS0',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='CS1/PS1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='CS2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='CS3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='CMOD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='6',name='VCC',func=Pin.PASSIVE,do_erc=True),
            Pin(num='7',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='8',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='9',name='SLD10',func=Pin.PASSIVE,do_erc=True),
            Pin(num='10',name='SLD11',func=Pin.PASSIVE,do_erc=True),
            Pin(num='20',name='CS4',func=Pin.PASSIVE,do_erc=True),
            Pin(num='11',name='SLD12',func=Pin.PASSIVE,do_erc=True),
            Pin(num='21',name='SDA',func=Pin.BIDIR,do_erc=True),
            Pin(num='12',name='SLD13',func=Pin.PASSIVE,do_erc=True),
            Pin(num='22',name='SCL',do_erc=True),
            Pin(num='13',name='SLD14',func=Pin.PASSIVE,do_erc=True),
            Pin(num='23',name='~HI~/BUZ',func=Pin.BIDIR,do_erc=True),
            Pin(num='14',name='CS11/SLD20',func=Pin.PASSIVE,do_erc=True),
            Pin(num='24',name='~XRES~',do_erc=True),
            Pin(num='15',name='CS12/SLD21',func=Pin.PASSIVE,do_erc=True),
            Pin(num='25',name='EP',func=Pin.PASSIVE,do_erc=True),
            Pin(num='16',name='CS13/SLD22',func=Pin.PASSIVE,do_erc=True),
            Pin(num='17',name='CS14/SLD23',func=Pin.PASSIVE,do_erc=True),
            Pin(num='18',name='CS15/SLD24',func=Pin.PASSIVE,do_erc=True),
            Pin(num='19',name='CS5/SH/~HI~',func=Pin.BIDIR,do_erc=True)]),
        Part(name='CY8CMBR3108',dest=TEMPLATE,tool=SKIDL,keywords='Touch Sensor 8ch',description='CapSense Controller, 8 Sensors, QFN-16+EP',ref_prefix='U',num_units=1,fplist=['QFN-16*'],do_erc=True,pins=[
            Pin(num='1',name='CS0/PS0',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='CS1/PS1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='CMOD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='VCC',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='VDDIO',func=Pin.PWRIN,do_erc=True),
            Pin(num='6',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='7',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='8',name='CS4/GPO0',func=Pin.PASSIVE,do_erc=True),
            Pin(num='9',name='CS5/GPO1',func=Pin.BIDIR,do_erc=True),
            Pin(num='10',name='CS6/GPO2',func=Pin.BIDIR,do_erc=True),
            Pin(num='11',name='CS7/GPO3/SH',func=Pin.BIDIR,do_erc=True),
            Pin(num='12',name='CS2/GUARD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='13',name='CS3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='14',name='SDA',func=Pin.BIDIR,do_erc=True),
            Pin(num='15',name='SCL',do_erc=True),
            Pin(num='16',name='~HI~/BUZ',func=Pin.BIDIR,do_erc=True),
            Pin(num='17',name='EP',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='CY8CMBR3110',dest=TEMPLATE,tool=SKIDL,keywords='Touch Sensor 10ch',description='CapSense Controller, 10 Sensors, SOIC-16',ref_prefix='U',num_units=1,fplist=['SOIC-16*'],do_erc=True,pins=[
            Pin(num='1',name='SDA',func=Pin.BIDIR,do_erc=True),
            Pin(num='2',name='SCL',do_erc=True),
            Pin(num='3',name='CS0/PS0',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='CS1/PS1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='CMOD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='6',name='VCC',func=Pin.PASSIVE,do_erc=True),
            Pin(num='7',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='8',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='9',name='CS5/GPO0',func=Pin.BIDIR,do_erc=True),
            Pin(num='10',name='CS6/GPO1',func=Pin.BIDIR,do_erc=True),
            Pin(num='11',name='CS7/GPO2',func=Pin.BIDIR,do_erc=True),
            Pin(num='12',name='CS8/GPO3',func=Pin.BIDIR,do_erc=True),
            Pin(num='13',name='CS2/GUARD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='14',name='CS9/GPO4/~HI~/BUZZ',func=Pin.BIDIR,do_erc=True),
            Pin(num='15',name='CS3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='16',name='CS4/SH',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='CY8CMBR3116',dest=TEMPLATE,tool=SKIDL,keywords='Touch Sensor 16ch',description='CapSense Controller, 16 Sensors, QFN-24+EP',ref_prefix='U',num_units=1,fplist=['QFN-24*'],do_erc=True,pins=[
            Pin(num='1',name='CS0/PS0',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='CS1/PS1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='CS2/GUARD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='CS3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='CMOD',func=Pin.PASSIVE,do_erc=True),
            Pin(num='6',name='VCC',func=Pin.PASSIVE,do_erc=True),
            Pin(num='7',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='8',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='9',name='CS15/SH/~HI~',func=Pin.BIDIR,do_erc=True),
            Pin(num='10',name='CS14/GPO6',func=Pin.BIDIR,do_erc=True),
            Pin(num='20',name='CS4',func=Pin.PASSIVE,do_erc=True),
            Pin(num='11',name='CS13/GPO5',func=Pin.BIDIR,do_erc=True),
            Pin(num='21',name='SDA',func=Pin.BIDIR,do_erc=True),
            Pin(num='12',name='CS12/GPO4',func=Pin.BIDIR,do_erc=True),
            Pin(num='22',name='SCL',do_erc=True),
            Pin(num='13',name='CS11/GPO3',func=Pin.BIDIR,do_erc=True),
            Pin(num='23',name='~HI~/BUZ/GPO7',func=Pin.BIDIR,do_erc=True),
            Pin(num='14',name='CS10/GPO2',func=Pin.BIDIR,do_erc=True),
            Pin(num='24',name='~XRES~',do_erc=True),
            Pin(num='15',name='CS9/GPO1',func=Pin.BIDIR,do_erc=True),
            Pin(num='25',name='EP',func=Pin.PASSIVE,do_erc=True),
            Pin(num='16',name='CS8/GPO0',func=Pin.BIDIR,do_erc=True),
            Pin(num='17',name='CS7',func=Pin.PASSIVE,do_erc=True),
            Pin(num='18',name='CS6',func=Pin.PASSIVE,do_erc=True),
            Pin(num='19',name='CS5',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='CYBL10563-68FNXIT',dest=TEMPLATE,tool=SKIDL,keywords='CYPRESS PROC BLE CY8BL ARM CORTEX M0 BLUETOOTH WLCSP',description='68-WLCSP, 48-MHz ARM® Cortex®-M0, 128KB Flash, 16kB SRAM, BLE 4.1, CAP-SENSE W/ GESTURES, 2 SCB, 4 TCPWM, I2S, 1 PWM , LCD, 1MSPS 12-BIT SAR',ref_prefix='U',num_units=1,fplist=['WLCSP_68'],do_erc=True,aliases=['CYBL10563-68FLXIT'],pins=[
            Pin(num='11',name='GANT1',func=Pin.PWRIN,do_erc=True),
            Pin(num='A1',name='VREF',func=Pin.PASSIVE,do_erc=True),
            Pin(num='B1',name='P2.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='C1',name='VSSA',func=Pin.PWRIN,do_erc=True),
            Pin(num='D1',name='P1.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='E1',name='P1.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='F1',name='VSSD',func=Pin.PWRIN,do_erc=True),
            Pin(num='G1',name='P0.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='H1',name='P0.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='J1',name='P0.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='A2',name='VSSA',func=Pin.PWRIN,do_erc=True),
            Pin(num='B2',name='VSSA',func=Pin.BIDIR,do_erc=True),
            Pin(num='C2',name='P2.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='D2',name='VDDA',func=Pin.PWRIN,do_erc=True),
            Pin(num='E2',name='P1.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='F2',name='P0.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='G2',name='VDDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='H2',name='P0.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='J2',name='P0.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='A3',name='P3.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='B3',name='P2.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='C3',name='P2.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='D3',name='P2.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='E3',name='P1.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='F3',name='P0.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='G3',name='P0.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='H3',name='XTAL24O',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J3',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='A4',name='P3.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='B4',name='P3.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='C4',name='P3.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='D4',name='P2.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='E4',name='P1.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='F4',name='P1.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='G4',name='VSSD',func=Pin.PWRIN,do_erc=True),
            Pin(num='H4',name='XTAL24I',do_erc=True),
            Pin(num='J4',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='A5',name='VSSD',func=Pin.PWRIN,do_erc=True),
            Pin(num='B5',name='P3.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='C5',name='P3.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='D5',name='P2.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='E5',name='P1.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='F5',name='P1.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='G5',name='VSSR',func=Pin.PWRIN,do_erc=True),
            Pin(num='H5',name='VSSR',func=Pin.PWRIN,do_erc=True),
            Pin(num='36',name='VDDA',func=Pin.PWRIN,do_erc=True),
            Pin(num='A6',name='VSSA',func=Pin.PWRIN,do_erc=True),
            Pin(num='B6',name='P3.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='C6',name='P3.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='D6',name='VSSD',func=Pin.PWRIN,do_erc=True),
            Pin(num='E6',name='P2.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='F6',name='VSSR',func=Pin.PWRIN,do_erc=True),
            Pin(num='G6',name='VSSR',func=Pin.PWRIN,do_erc=True),
            Pin(num='H6',name='VSSR',func=Pin.PWRIN,do_erc=True),
            Pin(num='57',name='GND_EP',func=Pin.PWRIN,do_erc=True),
            Pin(num='A7',name='VCCD',func=Pin.PWROUT,do_erc=True),
            Pin(num='B7',name='XTAL32I/P6.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='C7',name='XRES',do_erc=True),
            Pin(num='D7',name='P4.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='E7',name='P5.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='F7',name='VSSR',func=Pin.PWRIN,do_erc=True),
            Pin(num='G7',name='GANT2',func=Pin.PWRIN,do_erc=True),
            Pin(num='H7',name='ANT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='J7',name='NC',func=Pin.NOCONNECT,do_erc=True),
            Pin(num='A8',name='VDDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='B8',name='XTAL32O/P6.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='C8',name='P4.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='D8',name='P5.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='E8',name='VSSD',func=Pin.PWRIN,do_erc=True),
            Pin(num='F8',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='G8',name='VSSR',func=Pin.PWRIN,do_erc=True)]),
        Part(name='CYBL10x6x-56LQxx',dest=TEMPLATE,tool=SKIDL,keywords='CYPRESS PROC BLE CY8BL ARM CORTEX M0 BLUETOOTH QFN',description='Programmable Radio-on-Chip With Bluetooth Low Energy, 48-MHz ARM® Cortex®-M0 , 56-QFN',ref_prefix='U',num_units=1,fplist=['QFN_56_1EP'],do_erc=True,aliases=['CYBL10161-56LQXI', 'CYBL10162-56LQXI', 'CYBL10163-56LQXI', 'CYBL10461-56LQXI', 'CYBL10462-56LQXI', 'CYBL10463-56LQXI', 'CYBL10561-56LQXI', 'CYBL10562-56LQXI', 'CYBL10563-56LQXI', 'CYBL10563-56LQXQ'],pins=[
            Pin(num='1',name='VDDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='2',name='XTAL32O/P6.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='3',name='XTAL32I/P6.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='4',name='XRES',do_erc=True),
            Pin(num='5',name='P4.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='6',name='P4.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='7',name='P5.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='8',name='P5.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='9',name='VSSD',func=Pin.PWRIN,do_erc=True),
            Pin(num='10',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='20',name='P0.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='30',name='P1.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='40',name='P2.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='50',name='P3.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='11',name='GANT1',func=Pin.PWRIN,do_erc=True),
            Pin(num='21',name='P0.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='31',name='P1.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='41',name='P2.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='51',name='P3.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='12',name='ANT',func=Pin.OUTPUT,do_erc=True),
            Pin(num='22',name='P0.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='32',name='P1.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='42',name='P2.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='52',name='P3.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='13',name='GANT2',func=Pin.PWRIN,do_erc=True),
            Pin(num='23',name='VDDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='33',name='P1.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='43',name='P2.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='53',name='P3.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='14',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='24',name='P0.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='34',name='P1.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='44',name='P2.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='54',name='P3.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='15',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='25',name='P0.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='35',name='P1.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='45',name='VREF',func=Pin.PASSIVE,do_erc=True),
            Pin(num='55',name='VSSA',func=Pin.PWRIN,do_erc=True),
            Pin(num='16',name='XTAL24I',do_erc=True),
            Pin(num='26',name='P0.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='36',name='VDDA',func=Pin.PWRIN,do_erc=True),
            Pin(num='46',name='VDDA',func=Pin.PWRIN,do_erc=True),
            Pin(num='56',name='VCCD',func=Pin.PWROUT,do_erc=True),
            Pin(num='17',name='XTAL24O',func=Pin.OUTPUT,do_erc=True),
            Pin(num='27',name='P0.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='37',name='P2.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='47',name='P3.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='57',name='GND_EP',func=Pin.PWRIN,do_erc=True),
            Pin(num='18',name='VDDR',func=Pin.PWRIN,do_erc=True),
            Pin(num='28',name='P1.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='38',name='P2.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='48',name='P3.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='19',name='P0.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='29',name='P1.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='39',name='P2.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='49',name='P3.2',func=Pin.BIDIR,do_erc=True)])])