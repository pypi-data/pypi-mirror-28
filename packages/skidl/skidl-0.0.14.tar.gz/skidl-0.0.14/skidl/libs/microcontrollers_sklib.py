from skidl import Pin, Part, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

microcontrollers = SchLib(tool=SKIDL).add_parts(*[
        Part(name='ADUC816',dest=TEMPLATE,tool=SKIDL,keywords='8051 CORE MCU ADC DAC',description='8KB Flash, 256B SRAM, 640B EEPROM, 16-bit ADC, 12-bit DAC, MQFP-52',ref_prefix='U',num_units=1,fplist=['MQFP*'],do_erc=True,pins=[
            Pin(num='1',name='P1.0(T2)',func=Pin.BIDIR,do_erc=True),
            Pin(num='2',name='P1.1(T2EX)',func=Pin.BIDIR,do_erc=True),
            Pin(num='3',name='P1.2(DAC/IEXC1)',func=Pin.BIDIR,do_erc=True),
            Pin(num='4',name='P1.3(AIN5/IEXC2)',func=Pin.BIDIR,do_erc=True),
            Pin(num='5',name='AVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='6',name='AGND',func=Pin.PWRIN,do_erc=True),
            Pin(num='7',name='REF-',func=Pin.PASSIVE,do_erc=True),
            Pin(num='8',name='REF+',func=Pin.PASSIVE,do_erc=True),
            Pin(num='9',name='P1.4(AIN1)',do_erc=True),
            Pin(num='10',name='P1.5(AIN2)',do_erc=True),
            Pin(num='20',name='DVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='30',name='(A10)P2.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='40',name='~EA~',func=Pin.BIDIR,do_erc=True),
            Pin(num='50',name='(AD5)P0.5',func=Pin.TRISTATE,do_erc=True),
            Pin(num='11',name='P1.6(AIN3)',do_erc=True),
            Pin(num='21',name='DGND',func=Pin.PWRIN,do_erc=True),
            Pin(num='31',name='(A11)P2.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='41',name='~PSEN~',func=Pin.OUTPUT,do_erc=True),
            Pin(num='51',name='(AD6)P0.6',func=Pin.TRISTATE,do_erc=True),
            Pin(num='12',name='P1.7(AIN4)',func=Pin.BIDIR,do_erc=True),
            Pin(num='22',name='(T0)P3.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='32',name='XTAL1',do_erc=True),
            Pin(num='42',name='ALE',func=Pin.OUTPUT,do_erc=True),
            Pin(num='52',name='(AD7)P0.7',func=Pin.TRISTATE,do_erc=True),
            Pin(num='13',name='~SS~',do_erc=True),
            Pin(num='23',name='(T1)P3.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='33',name='XTAL2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='43',name='(AD0)P0.0',func=Pin.TRISTATE,do_erc=True),
            Pin(num='14',name='MISO',do_erc=True),
            Pin(num='24',name='(~WR~)P3.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='34',name='DVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='44',name='(AD1)P0.1',func=Pin.TRISTATE,do_erc=True),
            Pin(num='15',name='RESET',do_erc=True),
            Pin(num='25',name='(~RD~)P3.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='35',name='DGND',func=Pin.PWRIN,do_erc=True),
            Pin(num='45',name='(AD2)P0.2',func=Pin.TRISTATE,do_erc=True),
            Pin(num='16',name='(RxD)P3.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='26',name='SCLOCK',func=Pin.BIDIR,do_erc=True),
            Pin(num='36',name='(A12)P2.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='46',name='(AD3)P0.3',func=Pin.TRISTATE,do_erc=True),
            Pin(num='17',name='(TxD)P3.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='27',name='SDATA/MOSI',func=Pin.BIDIR,do_erc=True),
            Pin(num='37',name='(A13)P2.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='47',name='DGND',func=Pin.PWRIN,do_erc=True),
            Pin(num='18',name='(~INT0~)P3.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='28',name='(A8)P2.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='38',name='(A14)P2.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='48',name='DVDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='19',name='(~INT1~)P3.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='29',name='(A9)P2.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='39',name='(A15)P2.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='49',name='(AD4)P0.4',func=Pin.TRISTATE,do_erc=True)]),
        Part(name='P89LPC832A1FA',dest=TEMPLATE,tool=SKIDL,keywords='Philips 8051 Turbo Core',description='P89LPC932A1FA, 8kB Flash, 256 SRAM, 8bit MCS51 2-cycle Core Microcontroller, PLCC-28',ref_prefix='U',num_units=1,fplist=['PLCC*'],do_erc=True,pins=[
            Pin(num='1',name='ICB/P2.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='2',name='OCD/P2.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='3',name='P0.0/CMP2/KBI0',func=Pin.BIDIR,do_erc=True),
            Pin(num='4',name='P1.7/OCC',func=Pin.BIDIR,do_erc=True),
            Pin(num='5',name='P1.6/OCB',func=Pin.BIDIR,do_erc=True),
            Pin(num='6',name='P1.5/~RST',func=Pin.BIDIR,do_erc=True),
            Pin(num='7',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='8',name='XTAL1/P3.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='9',name='CLKOUT/XTAL2/P3.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='10',name='P1.4/~INT1',func=Pin.BIDIR,do_erc=True),
            Pin(num='20',name='P0.6/CMP1/KBI6',func=Pin.BIDIR,do_erc=True),
            Pin(num='11',name='P1.3/~INT0~/SDA',func=Pin.BIDIR,do_erc=True),
            Pin(num='21',name='VDD',func=Pin.PWRIN,do_erc=True),
            Pin(num='12',name='P1.2/T0/SCL',func=Pin.BIDIR,do_erc=True),
            Pin(num='22',name='P0.5/CMPREF/KBI5',func=Pin.BIDIR,do_erc=True),
            Pin(num='13',name='MOSI/P2.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='23',name='P0.4/CIN1A/KBI4',func=Pin.BIDIR,do_erc=True),
            Pin(num='14',name='MISO/P2.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='24',name='P0.3/CIN1B/KBI3',func=Pin.BIDIR,do_erc=True),
            Pin(num='15',name='~SS~/P2.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='25',name='P0.2/CIN2A/KBI2',func=Pin.BIDIR,do_erc=True),
            Pin(num='16',name='SPICLK/P2.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='26',name='P0.1/CIN2B/KBI1',func=Pin.BIDIR,do_erc=True),
            Pin(num='17',name='P1.1/RXD',func=Pin.BIDIR,do_erc=True),
            Pin(num='27',name='OCA/P2.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='18',name='P1.0/TXD',func=Pin.BIDIR,do_erc=True),
            Pin(num='28',name='ICA/P2.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='19',name='P0.7/T1/KB7',func=Pin.BIDIR,do_erc=True)]),
        Part(name='SAB80C515-M',dest=TEMPLATE,tool=SKIDL,keywords='CMOS MCU 8-bit',description='8KB ROM, 256B RAM, 8-bit CMOS High Performace Single-Chip Microcontroller, PMQFP-80',ref_prefix='U',num_units=1,fplist=['PLCC*'],do_erc=True,aliases=['SAB80C535-M'],pins=[
            Pin(num='1',name='~RESET~',do_erc=True),
            Pin(num='3',name='VAREF',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='VAGND',func=Pin.PWRIN,do_erc=True),
            Pin(num='5',name='AN7/P6.7',do_erc=True),
            Pin(num='6',name='AN6/P6.6',do_erc=True),
            Pin(num='7',name='AN5/P6.5',do_erc=True),
            Pin(num='8',name='AN4/P6.4',do_erc=True),
            Pin(num='9',name='AN3/P6.3',do_erc=True),
            Pin(num='10',name='AN2/P6.2',do_erc=True),
            Pin(num='20',name='P3.5/T1',func=Pin.BIDIR,do_erc=True),
            Pin(num='30',name='P1.1/INT4/CC1',func=Pin.BIDIR,do_erc=True),
            Pin(num='40',name='P2.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='60',name='P5.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='80',name='P4.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='11',name='AN1/P6.1',do_erc=True),
            Pin(num='21',name='P3.6/~WR~',func=Pin.BIDIR,do_erc=True),
            Pin(num='31',name='P1.0/~INT3~/CC0',func=Pin.BIDIR,do_erc=True),
            Pin(num='41',name='P2.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='61',name='P5.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='12',name='AN0/P6.0',do_erc=True),
            Pin(num='22',name='P3.7/~RD~',func=Pin.BIDIR,do_erc=True),
            Pin(num='42',name='P2.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='52',name='P0.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='62',name='P5.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='72',name='P4.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='33',name='VCC',func=Pin.PWRIN,do_erc=True),
            Pin(num='43',name='P2.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='53',name='P0.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='63',name='P5.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='73',name='P4.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='24',name='P1.7/T2',func=Pin.BIDIR,do_erc=True),
            Pin(num='34',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='44',name='P2.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='54',name='P0.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='64',name='P5.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='74',name='P4.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='15',name='P3.0/RXD',func=Pin.BIDIR,do_erc=True),
            Pin(num='25',name='P1.6/CLKOUT',func=Pin.BIDIR,do_erc=True),
            Pin(num='45',name='P2.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='55',name='P0.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='65',name='P5.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='75',name='~PE~',do_erc=True),
            Pin(num='16',name='P3.1/TXD',func=Pin.BIDIR,do_erc=True),
            Pin(num='26',name='P1.5/T2EX',func=Pin.BIDIR,do_erc=True),
            Pin(num='36',name='XTAL2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='56',name='P0.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='66',name='P5.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='76',name='P4.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='17',name='P3.2/~INT0~',func=Pin.BIDIR,do_erc=True),
            Pin(num='27',name='P1.4/~INT2~',func=Pin.BIDIR,do_erc=True),
            Pin(num='37',name='XTAL1',do_erc=True),
            Pin(num='47',name='~PSEN~',func=Pin.OUTPUT,do_erc=True),
            Pin(num='57',name='P0.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='67',name='P5.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='77',name='P4.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='18',name='P3.3/~INT1~',func=Pin.BIDIR,do_erc=True),
            Pin(num='28',name='P1.3/INT6/CC3',func=Pin.BIDIR,do_erc=True),
            Pin(num='38',name='P2.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='48',name='ALE',func=Pin.OUTPUT,do_erc=True),
            Pin(num='58',name='P0.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='78',name='P4.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='19',name='P3.4/T0',func=Pin.BIDIR,do_erc=True),
            Pin(num='29',name='P1.2/INT5/CC2',func=Pin.BIDIR,do_erc=True),
            Pin(num='39',name='P2.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='49',name='~EA~',do_erc=True),
            Pin(num='59',name='P0.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='69',name='VCC',func=Pin.PWRIN,do_erc=True),
            Pin(num='79',name='P4.6',func=Pin.BIDIR,do_erc=True)]),
        Part(name='SAB80C515-N',dest=TEMPLATE,tool=SKIDL,keywords='CMOS MCU 8-bit',description='SAB80C515-XX-N, 8KB ROM, 256B RAM, 8-bit CMOS High Performace Single-Chip Microcontroller, PLCC-68',ref_prefix='U',num_units=1,fplist=['PLCC*'],do_erc=True,aliases=['SAB80C535-N', 'SAB80C515-XX-N', 'SAB80C535-XX-N'],pins=[
            Pin(num='1',name='P4.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='2',name='P4.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='3',name='P4.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='4',name='~PE~',do_erc=True),
            Pin(num='5',name='P4.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='6',name='P4.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='7',name='P4.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='8',name='P4.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='9',name='P4.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='10',name='~RESET~',do_erc=True),
            Pin(num='20',name='AN0/P6.0',do_erc=True),
            Pin(num='30',name='P1.6/CLKOUT',func=Pin.BIDIR,do_erc=True),
            Pin(num='40',name='XTAL1',do_erc=True),
            Pin(num='50',name='ALE',func=Pin.OUTPUT,do_erc=True),
            Pin(num='60',name='P5.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='11',name='VAREF',func=Pin.PASSIVE,do_erc=True),
            Pin(num='21',name='P3.0/RXD',func=Pin.BIDIR,do_erc=True),
            Pin(num='31',name='P1.5/T2EX',func=Pin.BIDIR,do_erc=True),
            Pin(num='41',name='P2.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='51',name='~EA~',do_erc=True),
            Pin(num='61',name='P5.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='12',name='VAGND',func=Pin.PWRIN,do_erc=True),
            Pin(num='22',name='P3.1/TXD',func=Pin.BIDIR,do_erc=True),
            Pin(num='32',name='P1.4/~INT2~',func=Pin.BIDIR,do_erc=True),
            Pin(num='42',name='P2.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='52',name='P0.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='62',name='P5.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='13',name='AN7/P6.7',do_erc=True),
            Pin(num='23',name='P3.2/~INT0~',func=Pin.BIDIR,do_erc=True),
            Pin(num='33',name='P1.3/INT6/CC3',func=Pin.BIDIR,do_erc=True),
            Pin(num='43',name='P2.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='53',name='P0.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='63',name='P5.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='14',name='AN6/P6.6',do_erc=True),
            Pin(num='24',name='P3.3/~INT1~',func=Pin.BIDIR,do_erc=True),
            Pin(num='34',name='P1.2/INT5/CC2',func=Pin.BIDIR,do_erc=True),
            Pin(num='44',name='P2.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='54',name='P0.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='64',name='P5.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='15',name='AN5/P6.5',do_erc=True),
            Pin(num='25',name='P3.4/T0',func=Pin.BIDIR,do_erc=True),
            Pin(num='35',name='P1.1/INT4/CC1',func=Pin.BIDIR,do_erc=True),
            Pin(num='45',name='P2.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='55',name='P0.3',func=Pin.BIDIR,do_erc=True),
            Pin(num='65',name='P5.2',func=Pin.BIDIR,do_erc=True),
            Pin(num='16',name='AN4/P6.4',do_erc=True),
            Pin(num='26',name='P3.5/T1',func=Pin.BIDIR,do_erc=True),
            Pin(num='36',name='P1.0/~INT3~/CC0',func=Pin.BIDIR,do_erc=True),
            Pin(num='46',name='P2.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='56',name='P0.4',func=Pin.BIDIR,do_erc=True),
            Pin(num='66',name='P5.1',func=Pin.BIDIR,do_erc=True),
            Pin(num='17',name='AN3/P6.3',do_erc=True),
            Pin(num='27',name='P3.6/~WR~',func=Pin.BIDIR,do_erc=True),
            Pin(num='37',name='VCC',func=Pin.PWRIN,do_erc=True),
            Pin(num='47',name='P2.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='57',name='P0.5',func=Pin.BIDIR,do_erc=True),
            Pin(num='67',name='P5.0',func=Pin.BIDIR,do_erc=True),
            Pin(num='18',name='AN2/P6.2',do_erc=True),
            Pin(num='28',name='P3.7/~RD~',func=Pin.BIDIR,do_erc=True),
            Pin(num='38',name='VSS',func=Pin.PWRIN,do_erc=True),
            Pin(num='48',name='P2.7',func=Pin.BIDIR,do_erc=True),
            Pin(num='58',name='P0.6',func=Pin.BIDIR,do_erc=True),
            Pin(num='68',name='VCC',func=Pin.PWRIN,do_erc=True),
            Pin(num='19',name='AN1/P6.1',do_erc=True),
            Pin(num='29',name='P1.7/T2',func=Pin.BIDIR,do_erc=True),
            Pin(num='39',name='XTAL2',func=Pin.OUTPUT,do_erc=True),
            Pin(num='49',name='~PSEN~',func=Pin.OUTPUT,do_erc=True),
            Pin(num='59',name='P0.7',func=Pin.BIDIR,do_erc=True)])])