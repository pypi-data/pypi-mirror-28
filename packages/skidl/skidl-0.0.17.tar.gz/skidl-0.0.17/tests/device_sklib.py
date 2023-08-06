from skidl import Pin, Part, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

device = SchLib(tool=SKIDL).add_parts(*[
        Part(name=u'Amperemeter_AC',dest=TEMPLATE,tool=SKIDL,keywords=u'Amperemeter AC',description=u'AC Amperemeter',ref_prefix=u'MES',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Amperemeter_DC',dest=TEMPLATE,tool=SKIDL,keywords=u'Amperemeter DC',description=u'DC Amperemeter',ref_prefix=u'MES',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Antenna',dest=TEMPLATE,tool=SKIDL,keywords=u'antenna',description=u'Antenna symbol',ref_prefix=u'AE',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',do_erc=True)]),
        Part(name=u'Antenna_Chip',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Antenna_Dipole',dest=TEMPLATE,tool=SKIDL,keywords=u'dipole antenna',description=u'Dipole Antenna symbol',ref_prefix=u'AE',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',do_erc=True),
            Pin(num=u'2',name=u'~',do_erc=True)]),
        Part(name=u'Antenna_Loop',dest=TEMPLATE,tool=SKIDL,keywords=u'loop antenna',description=u'Loop Antenna symbol',ref_prefix=u'AE',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',do_erc=True),
            Pin(num=u'2',name=u'~',do_erc=True)]),
        Part(name=u'Antenna_Shield',dest=TEMPLATE,tool=SKIDL,keywords=u'antenna',description=u'Antenna symbol with extra pin for shielding',ref_prefix=u'AE',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',do_erc=True),
            Pin(num=u'2',name=u'Shield',do_erc=True)]),
        Part(name=u'Battery',dest=TEMPLATE,tool=SKIDL,keywords=u'batt voltage-source cell',description=u'Battery (multiple cells)',ref_prefix=u'BT',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'+',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'-',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Battery_Cell',dest=TEMPLATE,tool=SKIDL,keywords=u'battery cell',description=u'single battery cell',ref_prefix=u'BT',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'+',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'-',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Buzzer',dest=TEMPLATE,tool=SKIDL,keywords=u'Quartz Resonator Ceramic',description=u'Buzzer, polar',ref_prefix=u'BZ',num_units=1,fplist=[u'*Buzzer*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'C',dest=TEMPLATE,tool=SKIDL,keywords=u'cap capacitor',description=u'Unpolarized capacitor',ref_prefix=u'C',num_units=1,fplist=[u'C_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'CP',dest=TEMPLATE,tool=SKIDL,keywords=u'cap capacitor',description=u'Polarised capacitor',ref_prefix=u'C',num_units=1,fplist=[u'CP_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'CP1',dest=TEMPLATE,tool=SKIDL,keywords=u'cap capacitor',description=u'Polarised capacitor',ref_prefix=u'C',num_units=1,fplist=[u'CP_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'CP1_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'cap capacitor',description=u'Polarised capacitor',ref_prefix=u'C',num_units=1,fplist=[u'CP_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'CP_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'cap capacitor',description=u'Polarised capacitor',ref_prefix=u'C',num_units=1,fplist=[u'CP_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'CTRIM',dest=TEMPLATE,tool=SKIDL,keywords=u'trimmer variable capacitor',description=u'Trimmable capacitor',ref_prefix=u'C',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'CTRIM_DIF',dest=TEMPLATE,tool=SKIDL,keywords=u'trimmer capacitor',description=u'Differential variable capacitor with two stators',ref_prefix=u'C',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'C_Feedthrough',dest=TEMPLATE,tool=SKIDL,keywords=u'EMI filter feedthrough capacitor',description=u'EMI filter, single capacitor',ref_prefix=u'C',num_units=1,do_erc=True,aliases=[u'EMI_Filter_C'],pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'C_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'capacitor cap',description=u'Unpolarized capacitor',ref_prefix=u'C',num_units=1,fplist=[u'C_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'C_Variable',dest=TEMPLATE,tool=SKIDL,keywords=u'trimmer capacitor',description=u'Variable capacitor',ref_prefix=u'C',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Two pin crystal',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_GND2',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Three pin crystal (GND on pin 2), e.g. in SMD package',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_GND23',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Four pin crystal (GND on pins 2 and 3), e.g. in SMD package',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_GND23_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Two pin crystal, two ground/package pins (pin2 and 3) small symbol',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_GND24',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Four pin crystal (GND on pins 2 and 4), e.g. in SMD package',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_GND24_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Two pin crystal, two ground/package pins (pin2 and 4) small symbol',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_GND2_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Two pin crystal, one ground/package pins (pin2) small symbol',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_GND3',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Three pin crystal (GND on pin 3), e.g. in SMD package',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_GND3_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Two pin crystal, one ground/package pins (pin3) small symbol',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Crystal_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'quartz ceramic resonator oscillator',description=u'Two pin crystal, small symbol',ref_prefix=u'Y',num_units=1,fplist=[u'Crystal*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Diode',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'DIAC',dest=TEMPLATE,tool=SKIDL,keywords=u'AC diode DIAC',description=u'diode for alternating current',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'DIAC_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'AC diode DIAC',description=u'diode for alternating current, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Diode, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Bridge_+-AA',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'D_Bridge_+A-A',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'D_Bridge_+AA-',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'D_Bridge_-A+A',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'D_Bridge_-AA+',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'D_Capacitance',dest=TEMPLATE,tool=SKIDL,keywords=u'capacitance diode varicap varactor',description=u'variable capacitance diode (varicap, varactor)',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Capacitance_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'capacitance diode varicap varactor',description=u'variable capacitance diode (varicap, varactor), alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Photo',dest=TEMPLATE,tool=SKIDL,keywords=u'photodiode diode opto',description=u'Photodiode',ref_prefix=u'D',num_units=1,fplist=[u'*photodiode*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Photo_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'photodiode diode opto',description=u'Photodiode, alternative symbol',ref_prefix=u'D',num_units=1,fplist=[u'*photodiode*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Radiation',dest=TEMPLATE,tool=SKIDL,keywords=u'radiation detector diode',description=u'semiconductor radiation detector',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Radiation_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'radiation detector diode',description=u'semiconductor radiation detector, alternativ symbol',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky',dest=TEMPLATE,tool=SKIDL,keywords=u'diode Schottky',description=u'Schottky diode',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_AAK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schotty SCHDPAK',description=u'Schottky diode, two anode pins',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A',do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_AKA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schotty SCHDPAK',description=u'Schottky diode, two anode pins',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A',do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_AKK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schotty SCHDPAK',description=u'Schottky diode, two cathode pins',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schotty',description=u'Schottky diode, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_KAA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schotty SCHDPAK',description=u'Schottky diode, two anode pins',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_KAK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schotty SCHDPAK',description=u'Schottky diode, two cathode pins',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_KKA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schotty SCHDPAK',description=u'Schottky diode, two cathode pins',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schottky',description=u'Schottky diode, small symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_Small_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'diode schottky',description=u'Schottky diode, small symbol, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_ACom_AKK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode, common anode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_ACom_KAK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode, common anode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_ACom_KKA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode, common anode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_KCom_AAK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode, common cathode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_KCom_AKA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode, common cathode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_KCom_KAA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode, common cathode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_Serial_ACK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_Serial_AKC',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'common',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_Serial_CAK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_Serial_CKA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_Serial_KAC',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'common',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Schottky_x2_Serial_KCA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual schottky diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Shockley',dest=TEMPLATE,tool=SKIDL,keywords=u'Shockley diode',description=u'Shockley Diode (PNPN Diode)',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_SiPM',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'D_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Diode, small symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Small_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Diode, small symbol, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_TVS',dest=TEMPLATE,tool=SKIDL,keywords=u'diode TVS thyrector',description=u'transient-voltage-suppression (TVS) diode',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_TVS_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'diode TVS thyrector',description=u'transient-voltage-suppression (TVS) diode, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_TVS_x2_AAC',dest=TEMPLATE,tool=SKIDL,keywords=u'diode TVS thyrector',description=u'dual transient-voltage-suppression (TVS) diode (center=pin3)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'common',do_erc=True)]),
        Part(name=u'D_TVS_x2_ACA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode TVS thyrector',description=u'dual transient-voltage-suppression (TVS) diode (center=pin2)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'common',do_erc=True),
            Pin(num=u'3',name=u'A2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_TVS_x2_CAA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode TVS thyrector',description=u'dual transient-voltage-suppression (TVS) diode (center=pin1)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'common',do_erc=True),
            Pin(num=u'2',name=u'A1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Temperature_Dependent',dest=TEMPLATE,tool=SKIDL,keywords=u'temperature sensor diode',description=u'temperature dependent diode',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Temperature_Dependent_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'temperature sensor diode',description=u'temperature dependent diode, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Tunnel',dest=TEMPLATE,tool=SKIDL,keywords=u'tunnel diode',description=u'Tunnel Diode (Esaki Diode)',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Tunnel_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'tunnel diode',description=u'Tunnel Diode (Esaki Diode), alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Unitunnel',dest=TEMPLATE,tool=SKIDL,keywords=u'unitunnel diode',description=u'Unitunnel Diode',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Unitunnel_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'unitunnel diode',description=u'Unitunnel Diode, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Zener',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Zener Diode',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Zener_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Zener Diode, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Zener_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Zener Diode, small symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_Zener_Small_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Zener Diode, small symbol, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'TO-???*', u'*SingleDiode', u'*_Diode_*', u'*SingleDiode*', u'D_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_ACom_AKK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode, common anode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_ACom_KAK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode, common anode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_ACom_KKA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode, common anode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_KCom_AAK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode, common cathode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_KCom_AKA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode, common cathode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_KCom_KAA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode, common cathode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_Serial_ACK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_Serial_AKC',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'common',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_Serial_CAK',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_Serial_CKA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_Serial_KAC',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'common',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'D_x2_Serial_KCA',dest=TEMPLATE,tool=SKIDL,keywords=u'diode',description=u'Dual diode',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Delay_Line',dest=TEMPLATE,tool=SKIDL,keywords=u'delay propogation retard impedance',description=u'Delay line',ref_prefix=u'L',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'COMMUN',do_erc=True)]),
        Part(name=u'EMI_Filter_CLC',dest=TEMPLATE,tool=SKIDL,keywords=u'EMI T-filter',description=u'EMI T-filter (CLC)',ref_prefix=u'FL',num_units=1,fplist=[u'Resonator*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'EMI_Filter_LCL',dest=TEMPLATE,tool=SKIDL,keywords=u'EMI T-filter',description=u'EMI T-filter (LCL)',ref_prefix=u'FL',num_units=1,fplist=[u'Resonator*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'EMI_Filter_LL',dest=TEMPLATE,tool=SKIDL,keywords=u'EMI filter',description=u'EMI 2-inductor-filter',ref_prefix=u'FL',num_units=1,fplist=[u'L_*', u'L_CommonMode*'],do_erc=True,aliases=[u'EMI_Filter_CommonMode'],pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Earphone',dest=TEMPLATE,tool=SKIDL,keywords=u'earphone speaker headphone',description=u'earphone, polar',ref_prefix=u'LS',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Electromagnetic_Actor',dest=TEMPLATE,tool=SKIDL,keywords=u'electromagnet coil inductor',description=u'electro-magnetic actor',ref_prefix=u'L',num_units=1,fplist=[u'Inductor_*', u'L_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Ferrite_Bead',dest=TEMPLATE,tool=SKIDL,keywords=u'L ferite bead inductor filter',description=u'Ferrite bead',ref_prefix=u'L',num_units=1,fplist=[u'Inductor_*', u'L_*', u'*Ferrite*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Ferrite_Bead_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'L ferite bead inductor filter',description=u'Ferrite bead, small symbol',ref_prefix=u'L',num_units=1,fplist=[u'Inductor_*', u'L_*', u'*Ferrite*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Frequency_Counter',dest=TEMPLATE,tool=SKIDL,keywords=u'Frequency Counter',description=u'Frequency Counter',ref_prefix=u'MES',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Fuse',dest=TEMPLATE,tool=SKIDL,keywords=u'Fuse',description=u'Fuse, generic',ref_prefix=u'F',num_units=1,fplist=[u'*Fuse*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Fuse_Polarized',dest=TEMPLATE,tool=SKIDL,keywords=u'Fuse',description=u'Fuse, generic',ref_prefix=u'F',num_units=1,fplist=[u'*Fuse*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PWRIN,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PWROUT,do_erc=True)]),
        Part(name=u'Fuse_Polarized_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'fuse',description=u'Fuse, polarised',ref_prefix=u'F',num_units=1,fplist=[u'SM*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PWRIN,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PWROUT,do_erc=True)]),
        Part(name=u'Fuse_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'fuse',description=u'Fuse, small symbol',ref_prefix=u'F',num_units=1,fplist=[u'SM*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Galvanometer',dest=TEMPLATE,tool=SKIDL,keywords=u'Galvanometer',description=u'Galvanometer',ref_prefix=u'MES',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Hall_Generator',dest=TEMPLATE,tool=SKIDL,keywords=u'Hall generator magnet',description=u'Hall generator',ref_prefix=u'HG',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'U1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'U2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'UH1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'UH2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Heater',dest=TEMPLATE,tool=SKIDL,keywords=u'heater R resistor',description=u'Resistive Heater',ref_prefix=u'R',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Jumper',dest=TEMPLATE,tool=SKIDL,keywords=u'jumper bridge link nc',description=u'Jumper, generic, normally closed',ref_prefix=u'JP',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Jumper_NC_Dual',dest=TEMPLATE,tool=SKIDL,keywords=u'jumper bridge link nc',description=u'Dual Jumper, normally closed',ref_prefix=u'JP',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Jumper_NC_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'jumper link bridge',description=u'Jumper, normally closed',ref_prefix=u'JP',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Jumper_NO_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'jumper link bridge',description=u'Jumper, normally open',ref_prefix=u'JP',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'L',dest=TEMPLATE,tool=SKIDL,keywords=u'inductor choke coil reactor magnetic',description=u'Inductor',ref_prefix=u'L',num_units=1,fplist=[u'Choke_*', u'*Coil*', u'Inductor_*', u'L_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode',description=u'LED generic',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode',description=u'LED generic, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_ARGB',dest=TEMPLATE,tool=SKIDL,keywords=u'led rgb diode',description=u'LED RGB, common anode (pin 1)',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'RK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'GK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'BK',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_BGRA',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'LED_CRGB',dest=TEMPLATE,tool=SKIDL,keywords=u'led rgb diode',description=u'LED RGB, Common Cathode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'RA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'GA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'BA',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_Dual_2pin',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode bicolor dual',description=u'LED dual, 2pin version',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'KA',do_erc=True),
            Pin(num=u'2',name=u'AK',do_erc=True)]),
        Part(name=u'LED_Dual_AAC',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode bicolor dual',description=u'LED dual, common cathode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',do_erc=True),
            Pin(num=u'2',name=u'A2',do_erc=True),
            Pin(num=u'3',name=u'K',do_erc=True)]),
        Part(name=u'LED_Dual_AACC',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode bicolor dual',description=u'LED dual, 4-pin',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',do_erc=True),
            Pin(num=u'2',name=u'A2',do_erc=True),
            Pin(num=u'3',name=u'K1',do_erc=True),
            Pin(num=u'4',name=u'K2',do_erc=True)]),
        Part(name=u'LED_Dual_ACA',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode bicolor dual',description=u'LED dual, common cathode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',do_erc=True),
            Pin(num=u'2',name=u'K',do_erc=True),
            Pin(num=u'3',name=u'A2',do_erc=True)]),
        Part(name=u'LED_Dual_ACAC',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode bicolor dual',description=u'LED dual, 4-pin',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',do_erc=True),
            Pin(num=u'2',name=u'K1',do_erc=True),
            Pin(num=u'3',name=u'A2',do_erc=True),
            Pin(num=u'4',name=u'K2',do_erc=True)]),
        Part(name=u'LED_Dual_CAC',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode bicolor dual',description=u'LED dual, common anode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K1',do_erc=True),
            Pin(num=u'2',name=u'A',do_erc=True),
            Pin(num=u'3',name=u'K2',do_erc=True)]),
        Part(name=u'LED_Dual_CCA',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode bicolor dual',description=u'LED dual, common anode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K1',do_erc=True),
            Pin(num=u'2',name=u'K2',do_erc=True),
            Pin(num=u'3',name=u'A',do_erc=True)]),
        Part(name=u'LED_PAD',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'LED_RABG',dest=TEMPLATE,tool=SKIDL,keywords=u'led rgb diode',description=u'LED RGB, common anode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'RK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'BK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'GK',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_RAGB',dest=TEMPLATE,tool=SKIDL,keywords=u'led rgb diode',description=u'LED RGB, common anode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'RK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'GK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'BK',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_RCBG',dest=TEMPLATE,tool=SKIDL,keywords=u'led rgb diode',description=u'LED RGB, Common Cathode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'RA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'BA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'GA',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_RCGB',dest=TEMPLATE,tool=SKIDL,keywords=u'led rgb diode',description=u'LED RGB, Common Cathode',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'RA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'GA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'BA',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_RGB',dest=TEMPLATE,tool=SKIDL,keywords=u'led rgb diode',description=u'LED RGB 6 pins',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'RK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'GK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'BK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'BA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'GA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'RA',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_RGB_EP',dest=TEMPLATE,tool=SKIDL,keywords=u'led rgb diode',description=u'LED RGB 6 pins, exposed pad',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'RK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'GK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'BK',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'BA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'GA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'RA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'PAD',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_Series',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'LED_Series_PAD',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'LED_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode light-emitting-diode',description=u'LED, small symbol',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LED_Small_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'led diode light-emitting-diode',description=u'LED, small symbol, alternativ symbol',ref_prefix=u'D',num_units=1,fplist=[u'LED*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'LTRIM',dest=TEMPLATE,tool=SKIDL,keywords=u'inductor choke coil reactor magnetic',description=u'Variable Inductor',ref_prefix=u'L',num_units=1,fplist=[u'Inductor_*', u'L_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'L_Core_Ferrite',dest=TEMPLATE,tool=SKIDL,keywords=u'inductor choke coil reactor magnetic',description=u'Inductor with Ferrite Core',ref_prefix=u'L',num_units=1,fplist=[u'Choke_*', u'*Coil*', u'Inductor_*', u'L_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'L_Core_Ferrite_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'inductor choke coil reactor magnetic',description=u'Inductor with ferrite core, small symbol',ref_prefix=u'L',num_units=1,fplist=[u'Choke_*', u'*Coil*', u'Inductor_*', u'L_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'L_Core_Iron',dest=TEMPLATE,tool=SKIDL,keywords=u'inductor choke coil reactor magnetic',description=u'Inductor with Iron Core',ref_prefix=u'L',num_units=1,fplist=[u'Choke_*', u'*Coil*', u'Inductor_*', u'L_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'L_Core_Iron_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'inductor choke coil reactor magnetic',description=u'Inductor with iron core, small symbol',ref_prefix=u'L',num_units=1,fplist=[u'Choke_*', u'*Coil*', u'Inductor_*', u'L_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'L_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'inductor choke coil reactor magnetic',description=u'Inductor, small symbol',ref_prefix=u'L',num_units=1,fplist=[u'Choke_*', u'*Coil*', u'Inductor_*', u'L_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Lamp',dest=TEMPLATE,tool=SKIDL,keywords=u'lamp',description=u'lamp',ref_prefix=u'LA',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Lamp_Flash',dest=TEMPLATE,tool=SKIDL,keywords=u'flash lamp',description=u'flash lamp tube',ref_prefix=u'LA',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Lamp_Neon',dest=TEMPLATE,tool=SKIDL,keywords=u'neon lamp',description=u'neon lamp',ref_prefix=u'NE',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Laserdiode_1A3C',dest=TEMPLATE,tool=SKIDL,keywords=u'opto laserdiode',description=u'Laser Diode in a 2-pin package',ref_prefix=u'LD',num_units=1,fplist=[u'*LaserDiode*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Laserdiode_1C2A',dest=TEMPLATE,tool=SKIDL,keywords=u'opto laserdiode',description=u'Laser Diode in a 2-pin package',ref_prefix=u'LD',num_units=1,fplist=[u'*LaserDiode*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Laserdiode_M_TYPE',dest=TEMPLATE,tool=SKIDL,keywords=u'opto laserdiode photodiode',description=u'Laser Diode in a 3-pin package with photodiode (1=LD-A, 2=LD-C/PD-C, 3=PD-A)',ref_prefix=u'LD',num_units=1,fplist=[u'*LaserDiode*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Laserdiode_N_TYPE',dest=TEMPLATE,tool=SKIDL,keywords=u'opto laserdiode photodiode',description=u'Laser Diode in a 3-pin package with photodiode (1=LD-C, 2=LD-A/PD-C, 3=PD-A)',ref_prefix=u'LD',num_units=1,fplist=[u'*LaserDiode*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Laserdiode_P_TYPE',dest=TEMPLATE,tool=SKIDL,keywords=u'opto laserdiode photodiode',description=u'Laser Diode in a 3-pin package with photodiode (1=LD-A, 2=LD-C/PD-A, 3=PD-C)',ref_prefix=u'LD',num_units=1,fplist=[u'*LaserDiode*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'MEMRISTOR',dest=TEMPLATE,tool=SKIDL,keywords=u'Memristor',description=u'Memristor',ref_prefix=u'MR',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Microphone',dest=TEMPLATE,tool=SKIDL,keywords=u'Microphone',description=u'Microphone',ref_prefix=u'MK',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Microphone_Condenser',dest=TEMPLATE,tool=SKIDL,keywords=u'Capacitance condenser Microphone',description=u'Condenser Microspcope',ref_prefix=u'MK',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Microphone_Crystal',dest=TEMPLATE,tool=SKIDL,keywords=u'Microphone Ultrasound crystal',description=u'Ultrasound receiver',ref_prefix=u'MK',num_units=1,do_erc=True,aliases=[u'Microphone_Ultrasound'],pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Net-Tie_2',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Net-Tie_3',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Net-Tie_3_Tee',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Net-Tie_4',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Net-Tie_4_Cross',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Ohmmeter',dest=TEMPLATE,tool=SKIDL,keywords=u'Ohmmeter',description=u'Ohmmeter, measures resistance',ref_prefix=u'MES',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Opamp_Dual_Generic',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Opamp_Quad_Generic',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Oscilloscope',dest=TEMPLATE,tool=SKIDL,keywords=u'Oscilloscope',description=u'Oscilloscope',ref_prefix=u'MES',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'POT',dest=TEMPLATE,tool=SKIDL,keywords=u'resistor variable',description=u'Potentionmeter',ref_prefix=u'RV',num_units=1,fplist=[u'Potentiometer*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'POT_Dual',dest=TEMPLATE,tool=SKIDL,keywords=u'resistor variable',description=u'Dual Potentionmeter',ref_prefix=u'RV',num_units=1,fplist=[u'Potentiometer*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'6',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'POT_Dual_Separate',dest=TEMPLATE,tool=SKIDL,keywords=u'resistor variable',description=u'Dual Potentionmeter, separate units',ref_prefix=u'RV',num_units=2,fplist=[u'Potentiometer*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'6',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'POT_TRIM',dest=TEMPLATE,tool=SKIDL,keywords=u'resistor variable trimpot trimmer',description=u'Trim-Potentionmeter',ref_prefix=u'RV',num_units=1,fplist=[u'Potentiometer*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Peltier_Element',dest=TEMPLATE,tool=SKIDL,keywords=u'Peltier TEC',description=u'Peltier Element, Thermoelectric Cooler (TEC)',ref_prefix=u'PE',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Polyfuse',dest=TEMPLATE,tool=SKIDL,keywords=u'resettable fuse PTC PPTC polyfuse polyswitch',description=u'resettable fuse, polymeric positive temperature coefficient (PPTC)',ref_prefix=u'F',num_units=1,fplist=[u'*polyfuse*', u'*PTC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Polyfuse_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'resettable fuse PTC PPTC polyfuse polyswitch',description=u'resettable fuse, polymeric positive temperature coefficient (PPTC), small symbol',ref_prefix=u'F',num_units=1,fplist=[u'*polyfuse*', u'*PTC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_DUAL_NPN_C2C1E1E2',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Q_DUAL_NPN_NPN_E1B1C2E2B2C1',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Q_DUAL_NPN_PNP_E1B1C2E2B2C1',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Q_DUAL_PNP_C2C1E1E2',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Q_DUAL_PNP_PNP_C1B1B2C2E2E1',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Q_DUAL_PNP_PNP_E1B1C2E2B2C1',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Q_NIGBT_CEG',dest=TEMPLATE,tool=SKIDL,keywords=u'igbt n-igbt transistor',description=u'Transistor N-IGBT (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_NIGBT_CGE',dest=TEMPLATE,tool=SKIDL,keywords=u'igbt n-igbt transistor',description=u'Transistor N-IGBT (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NIGBT_ECG',dest=TEMPLATE,tool=SKIDL,keywords=u'igbt n-igbt transistor',description=u'Transistor N-IGBT (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_NIGBT_ECGC',dest=TEMPLATE,tool=SKIDL,keywords=u'igbt n-igbt transistor',description=u'Transistor N-IGBT, collector connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True),
            Pin(num=u'4',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NIGBT_EGC',dest=TEMPLATE,tool=SKIDL,keywords=u'igbt n-igbt transistor',description=u'Transistor N-IGBT (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NIGBT_GCE',dest=TEMPLATE,tool=SKIDL,keywords=u'igbt n-igbt transistor',description=u'Transistor N-IGBT (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NIGBT_GCEC',dest=TEMPLATE,tool=SKIDL,keywords=u'igbt n-igbt transistor',description=u'Transistor N-IGBT, collector connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NIGBT_GEC',dest=TEMPLATE,tool=SKIDL,keywords=u'igbt n-igbt transistor',description=u'Transistor N-IGBT (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NJFET_DGS',dest=TEMPLATE,tool=SKIDL,keywords=u'njfet n-jfet transistor',description=u'Transistor N-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NJFET_DSG',dest=TEMPLATE,tool=SKIDL,keywords=u'njfet n-jfet transistor',description=u'Transistor N-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_NJFET_GDS',dest=TEMPLATE,tool=SKIDL,keywords=u'njfet n-jfet transistor',description=u'Transistor N-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NJFET_GSD',dest=TEMPLATE,tool=SKIDL,keywords=u'njfet n-jfet transistor',description=u'Transistor N-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NJFET_SDG',dest=TEMPLATE,tool=SKIDL,keywords=u'njfet n-jfet transistor',description=u'Transistor N-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_NJFET_SGD',dest=TEMPLATE,tool=SKIDL,keywords=u'njfet n-jfet transistor',description=u'Transistor N-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NMOS_DGS',dest=TEMPLATE,tool=SKIDL,keywords=u'nmos n-mos n-mosfet transistor',description=u'Transistor N-MOSFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NMOS_DSG',dest=TEMPLATE,tool=SKIDL,keywords=u'NMOS n-mos n-mosfet transistor',description=u'Transistor N-MOSFET with substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_NMOS_GDS',dest=TEMPLATE,tool=SKIDL,keywords=u'nmos n-mos n-mosfet transistor',description=u'Transistor N-MOSFET with substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NMOS_GDSD',dest=TEMPLATE,tool=SKIDL,keywords=u'NMOS n-mos n-mosfet transistor',description=u'Transistor N-MOSFETwith substrate diode, drain connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NMOS_GSD',dest=TEMPLATE,tool=SKIDL,keywords=u'NMOS n-mos n-mosfet transistor',description=u'Transistor N-MOSFETwith substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NMOS_SDG',dest=TEMPLATE,tool=SKIDL,keywords=u'NMOS n-mos n-mosfet transistor',description=u'Transistor N-MOSFETwith substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_NMOS_SDGD',dest=TEMPLATE,tool=SKIDL,keywords=u'NMOS n-mos n-mosfet transistor',description=u'Transistor N-MOSFETwith substrate diode, drain connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True),
            Pin(num=u'4',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NMOS_SGD',dest=TEMPLATE,tool=SKIDL,keywords=u'NMOS n-mos n-mosfet transistor',description=u'Transistor N-MOSFETwith substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_BCE',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor',description=u'Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_BCEC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor',description=u'Transistor NPN, collector connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_BEC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor',description=u'Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_CBE',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor',description=u'Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_CEB',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor',description=u'Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True)]),
        Part(name=u'Q_NPN_Darlington_BCE',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor darlington',description=u'Darlington Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_Darlington_BCEC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor darlington',description=u'Darlington Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'C2',do_erc=True)]),
        Part(name=u'Q_NPN_Darlington_BEC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor darlington',description=u'Darlington Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_Darlington_CBE',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor darlington',description=u'Darlington Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_Darlington_CEB',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor darlington',description=u'Darlington Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True)]),
        Part(name=u'Q_NPN_Darlington_EBC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor darlington',description=u'Darlington Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_Darlington_ECB',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor darlington',description=u'Darlington Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_Darlington_ECBC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor darlington',description=u'Darlington Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'C2',do_erc=True)]),
        Part(name=u'Q_NPN_EBC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor',description=u'Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_ECB',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor',description=u'Transistor NPN (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NPN_ECBC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn transistor',description=u'Transistor NPN, collector connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_NUJT_BEB',dest=TEMPLATE,tool=SKIDL,keywords=u'UJT transistor',description=u'Transistor N-Type Unijunction (UJT, general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'E',do_erc=True),
            Pin(num=u'3',name=u'B1',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PJFET_DGS',dest=TEMPLATE,tool=SKIDL,keywords=u'pjfet p-jfet transistor',description=u'Transistor P-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PJFET_DSG',dest=TEMPLATE,tool=SKIDL,keywords=u'pjfet p-jfet transistor',description=u'Transistor P-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_PJFET_GDS',dest=TEMPLATE,tool=SKIDL,keywords=u'pjfet p-jfet transistor',description=u'Transistor P-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PJFET_GSD',dest=TEMPLATE,tool=SKIDL,keywords=u'pjfet p-jfet transistor',description=u'Transistor P-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PJFET_SDG',dest=TEMPLATE,tool=SKIDL,keywords=u'pjfet p-jfet transistor',description=u'Transistor P-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_PJFET_SGD',dest=TEMPLATE,tool=SKIDL,keywords=u'pjfet p-jfet transistor',description=u'Transistor P-JFET (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PMOS_DGS',dest=TEMPLATE,tool=SKIDL,keywords=u'pmos p-mos p-mosfet transistor',description=u'Transistor P-MOSFET with substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PMOS_DSG',dest=TEMPLATE,tool=SKIDL,keywords=u'pmos p-mos p-mosfet transistor',description=u'Transistor P-MOSFET with substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_PMOS_GDS',dest=TEMPLATE,tool=SKIDL,keywords=u'pmos p-mos p-mosfet transistor',description=u'Transistor P-MOSFET with substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PMOS_GDSD',dest=TEMPLATE,tool=SKIDL,keywords=u'pmos p-mos p-mosfet transistor',description=u'Transistor P-MOSFET with substrate diode, drain connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PMOS_GSD',dest=TEMPLATE,tool=SKIDL,keywords=u'pmos p-mos p-mosfet transistor',description=u'Transistor P-MOSFET with substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PMOS_SDG',dest=TEMPLATE,tool=SKIDL,keywords=u'pmos p-mos p-mosfet transistor',description=u'Transistor P-MOSFET with substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_PMOS_SDGD',dest=TEMPLATE,tool=SKIDL,keywords=u'pmos p-mos p-mosfet transistor',description=u'Transistor P-MOSFET with substrate diode, drain connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'D',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True),
            Pin(num=u'4',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PMOS_SGD',dest=TEMPLATE,tool=SKIDL,keywords=u'pmos p-mos p-mosfet transistor',description=u'Transistor P-MOSFET with substrate diode (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'S',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'D',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_BCE',dest=TEMPLATE,tool=SKIDL,keywords=u'pnp transistor',description=u'Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_BCEC',dest=TEMPLATE,tool=SKIDL,keywords=u'pnp transistor',description=u'Transistor PNP, collector connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_BEC',dest=TEMPLATE,tool=SKIDL,keywords=u'pnp transistor',description=u'Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_CBE',dest=TEMPLATE,tool=SKIDL,keywords=u'pnp transistor',description=u'Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_CEB',dest=TEMPLATE,tool=SKIDL,keywords=u'pnp transistor',description=u'Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True)]),
        Part(name=u'Q_PNP_Darlington_BCE',dest=TEMPLATE,tool=SKIDL,keywords=u'PNP transistor darlington',description=u'Darlington Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_Darlington_BCEC',dest=TEMPLATE,tool=SKIDL,keywords=u'PNP transistor darlington',description=u'Darlington Transistor PNP, collector connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_Darlington_BEC',dest=TEMPLATE,tool=SKIDL,keywords=u'PNP transistor darlington',description=u'Darlington Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B',do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_Darlington_CBE',dest=TEMPLATE,tool=SKIDL,keywords=u'PNP transistor darlington',description=u'Darlington Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_Darlington_CEB',dest=TEMPLATE,tool=SKIDL,keywords=u'PNP transistor darlington',description=u'Darlington Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True)]),
        Part(name=u'Q_PNP_Darlington_EBC',dest=TEMPLATE,tool=SKIDL,keywords=u'PNP transistor darlington',description=u'Darlington Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_Darlington_ECB',dest=TEMPLATE,tool=SKIDL,keywords=u'PNP transistor darlington',description=u'Darlington Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True)]),
        Part(name=u'Q_PNP_Darlington_ECBC',dest=TEMPLATE,tool=SKIDL,keywords=u'PNP transistor darlington',description=u'Darlington Transistor PNP, collector connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True),
            Pin(num=u'4',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_EBC',dest=TEMPLATE,tool=SKIDL,keywords=u'pnp transistor',description=u'Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PNP_ECB',dest=TEMPLATE,tool=SKIDL,keywords=u'pnp transistor',description=u'Transistor PNP (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True)]),
        Part(name=u'Q_PNP_ECBC',dest=TEMPLATE,tool=SKIDL,keywords=u'pnp transistor',description=u'Transistor PNP, collector connected to mounting plane (general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True),
            Pin(num=u'4',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_PUJT_BEB',dest=TEMPLATE,tool=SKIDL,keywords=u'UJT transistor',description=u'Transistor P-Type Unijunction (UJT, general)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'B2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'E',do_erc=True),
            Pin(num=u'3',name=u'B1',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_Photo_NPN',dest=TEMPLATE,tool=SKIDL,keywords=u'npn phototransistor',description=u'Phototransistor NPN, 2-pin (C=1, E=2)',ref_prefix=u'Q',num_units=1,do_erc=True,aliases=[u'Q_Photo_NPN_CE'],pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_Photo_NPN_CBE',dest=TEMPLATE,tool=SKIDL,keywords=u'npn phototransistor',description=u'Phototransistor NPN, 3-pin with base pin (C=1, B=2, E=3)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'C',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',do_erc=True),
            Pin(num=u'3',name=u'E',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_Photo_NPN_EBC',dest=TEMPLATE,tool=SKIDL,keywords=u'npn phototransistor',description=u'Phototransistor NPN, 3-pin with base pin (E=1, B=2, C=3)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'B',do_erc=True),
            Pin(num=u'3',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_Photo_NPN_EC',dest=TEMPLATE,tool=SKIDL,keywords=u'NPN phototransistor',description=u'Phototransistor NPN, 2-pin (C=1, E=2)',ref_prefix=u'Q',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'E',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_TRIAC_AAG',dest=TEMPLATE,tool=SKIDL,keywords=u'triode for alternating current TRIAC',description=u'triode for alternating current (TRIAC)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_TRIAC_AGA',dest=TEMPLATE,tool=SKIDL,keywords=u'triode for alternating current TRIAC',description=u'triode for alternating current (TRIAC)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'A2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_TRIAC_GAA',dest=TEMPLATE,tool=SKIDL,keywords=u'triode for alternating current TRIAC',description=u'triode for alternating current (TRIAC)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'A1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_Thyristor_AGK',dest=TEMPLATE,tool=SKIDL,keywords=u'Thyristor silicon controlled rectifier',description=u'silicon controlled rectifier (Thyristor)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_Thyristor_AKG',dest=TEMPLATE,tool=SKIDL,keywords=u'Thyristor silicon controlled rectifier',description=u'silicon controlled rectifier (Thyristor)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_Thyristor_GAK',dest=TEMPLATE,tool=SKIDL,keywords=u'Thyristor silicon controlled rectifier',description=u'silicon controlled rectifier (Thyristor)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'K',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_Thyristor_GKA',dest=TEMPLATE,tool=SKIDL,keywords=u'Thyristor silicon controlled rectifier',description=u'silicon controlled rectifier (Thyristor)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'G',do_erc=True),
            Pin(num=u'2',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Q_Thyristor_KAG',dest=TEMPLATE,tool=SKIDL,keywords=u'Thyristor silicon controlled rectifier',description=u'silicon controlled rectifier (Thyristor)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'G',do_erc=True)]),
        Part(name=u'Q_Thyristor_KGA',dest=TEMPLATE,tool=SKIDL,keywords=u'Thyristor silicon controlled rectifier',description=u'silicon controlled rectifier (Thyristor)',ref_prefix=u'D',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'K',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'G',do_erc=True),
            Pin(num=u'3',name=u'A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R',dest=TEMPLATE,tool=SKIDL,keywords=u'r res resistor',description=u'Resistor',ref_prefix=u'R',num_units=1,fplist=[u'R_*', u'R_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'RF_Shield_One_Piece',dest=TEMPLATE,tool=SKIDL,keywords=u'RF EMI Shielding Cabinet',description=u'One-Piece EMI RF Shielding Cabinet',ref_prefix=u'J',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'Shield',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'RF_Shield_Two_Pieces',dest=TEMPLATE,tool=SKIDL,keywords=u'RF EMI Shielding Cabinet',description=u'Two-Piece EMI RF Shielding Cabinet',ref_prefix=u'J',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'Shield',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'RTRIM',dest=TEMPLATE,tool=SKIDL,keywords=u'r res resistor variable potentiometer trimmer',description=u'trimmable Resistor (Preset resistor)',ref_prefix=u'R',num_units=1,fplist=[u'R_*', u'R_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network03',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'3 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network04',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'4 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network05',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'5 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network06',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'6 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network07',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'7 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network08',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'8 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network09',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'9 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network10',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'10 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R10',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network11',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'11 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R10',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R11',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network12',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'12 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R10',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R11',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'R12',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network13',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network star-topology',description=u'13 Resistor network, star topology, bussed resistors, small symbol',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'common',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R10',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R11',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'R12',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'14',name=u'R13',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x02_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'2 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x03_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'3 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x04_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'4 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x05_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'5 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x06_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'6 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x07_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'7 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x08_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'8 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x09_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'9 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x10_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'10 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R10',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Network_Dividers_x11_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network divider topology',description=u'11 Voltage Dividers network, Dual Terminator, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'COM1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R10',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R11',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'COM2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_PHOTO',dest=TEMPLATE,tool=SKIDL,keywords=u'resistor variable light opto LDR',description=u'Photoresistor, light sensitive resistor, LDR',ref_prefix=u'R',num_units=1,fplist=[u'R?', u'R?-*', u'LDR*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack02',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'2 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R1.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack02_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'2 Resistor network, parallel topology, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R2.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack03',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'3 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R1.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack03_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'3 Resistor network, parallel topology, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R3.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack04',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'4 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R1.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack04_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'4 Resistor network, parallel topology, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R4.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack05',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'5 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R1.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack05_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'5 Resistor network, parallel topology, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R5.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack06',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'6 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R6.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R6.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R1.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack06_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'6 Resistor network, parallel topology, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R6.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R6.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack07',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'7 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R6.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R7.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R7.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R6.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'14',name=u'R1.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack07_SIP',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'7 Resistor network, parallel topology, SIP package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R1.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R6.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R6.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'R7.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'14',name=u'R7.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack08',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'8 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R6.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R7.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R8.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R8.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R7.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R6.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'14',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'15',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'16',name=u'R1.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack09',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'9 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R6.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R7.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R8.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R9.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R9.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R8.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R7.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'R6.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'14',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'15',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'16',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'17',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'18',name=u'R1.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack10',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'10 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R6.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R7.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R8.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R9.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R10.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'20',name=u'R1.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R10.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R9.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'R8.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'14',name=u'R7.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'15',name=u'R6.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'16',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'17',name=u'R4.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'18',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'19',name=u'R2.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Pack11',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network parallel topology',description=u'11 Resistor network, parallel topology, DIP package',ref_prefix=u'RN',num_units=1,fplist=[u'DIP*', u'SOIC*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'R1.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'R2.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'R3.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'R4.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'R5.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'R6.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'R7.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'R8.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'9',name=u'R9.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'10',name=u'R10.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'20',name=u'R3.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'11',name=u'R11.1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'21',name=u'R2.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'12',name=u'R11.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'22',name=u'R1.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'13',name=u'R10.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'14',name=u'R9.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'15',name=u'R8.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'16',name=u'R7.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'17',name=u'R6.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'18',name=u'R5.2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'19',name=u'R4.2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Shunt',dest=TEMPLATE,tool=SKIDL,keywords=u'r res shunt resistor',description=u'Shunt Resistor',ref_prefix=u'R',num_units=1,fplist=[u'R_*Shunt*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'r resistor',description=u'Resistor, small symbol',ref_prefix=u'R',num_units=1,fplist=[u'R_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'R_Variable',dest=TEMPLATE,tool=SKIDL,keywords=u'r res resistor variable potentiometer',description=u'variable Resistor (Rheostat)',ref_prefix=u'R',num_units=1,fplist=[u'R_*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Resonator',dest=TEMPLATE,tool=SKIDL,keywords=u'Ceramic Resonator',description=u'Three pin ceramic resonator',ref_prefix=u'Y',num_units=1,fplist=[u'Resonator*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Resonator_Small',dest=TEMPLATE,tool=SKIDL,keywords=u'Ceramic Resonator',description=u'Three pin ceramic resonator',ref_prefix=u'Y',num_units=1,fplist=[u'Resonator*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Rotary_Encoder',dest=TEMPLATE,tool=SKIDL,keywords=u'rotary switch encoder',description=u'Rotary encoder, dual channel, incremental quadrate outputs',ref_prefix=u'SW',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',do_erc=True),
            Pin(num=u'2',name=u'C',do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True)]),
        Part(name=u'Rotary_Encoder_Switch',dest=TEMPLATE,tool=SKIDL,keywords=u'rotary switch encoder switch push button',description=u'Rotary encoder, dual channel, incremental quadrate outputs, with switch',ref_prefix=u'SW',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'A',do_erc=True),
            Pin(num=u'2',name=u'C',do_erc=True),
            Pin(num=u'3',name=u'B',do_erc=True),
            Pin(num=u'4',name=u'~',do_erc=True),
            Pin(num=u'5',name=u'~',do_erc=True)]),
        Part(name=u'SPARK_GAP',dest=TEMPLATE,tool=SKIDL,do_erc=True),
        Part(name=u'Solar_Cell',dest=TEMPLATE,tool=SKIDL,keywords=u'solar cell',description=u'single solar cell',ref_prefix=u'SC',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'+',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'-',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Solar_Cells',dest=TEMPLATE,tool=SKIDL,keywords=u'solar cell',description=u'multiple solar cells',ref_prefix=u'SC',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'+',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'-',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Speaker',dest=TEMPLATE,tool=SKIDL,keywords=u'speaker sound',description=u'speaker',ref_prefix=u'LS',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'1',do_erc=True),
            Pin(num=u'2',name=u'2',do_erc=True)]),
        Part(name=u'Speaker_Crystal',dest=TEMPLATE,tool=SKIDL,keywords=u'crystal speaker ultrasonic transducer',description=u'ultrasonic transducer',ref_prefix=u'LS',num_units=1,do_erc=True,aliases=[u'Speaker_Ultrasound'],pins=[
            Pin(num=u'1',name=u'1',do_erc=True),
            Pin(num=u'2',name=u'2',do_erc=True)]),
        Part(name=u'Thermistor',dest=TEMPLATE,tool=SKIDL,keywords=u'r res thermistor',description=u'Thermistor, temperature-dependent resistor',ref_prefix=u'TH',num_units=1,fplist=[u'R_*', u'SM0603', u'SM0805'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermistor_NTC',dest=TEMPLATE,tool=SKIDL,keywords=u'thermistor NTC resistor sensor RTD',description=u'temperature dependent resistor, negative temperature coefficient (NTC)',ref_prefix=u'TH',num_units=1,fplist=[u'*NTC*', u'*Thermistor*', u'PIN?ARRAY*', u'bornier*', u'*Terminal?Block*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermistor_NTC_3wire',dest=TEMPLATE,tool=SKIDL,keywords=u'thermistor NTC resistor sensor RTD',description=u'temperature dependent resistor, negative temperature coefficient (NTC), 3-wire interface',ref_prefix=u'TH',num_units=1,fplist=[u'*NTC*', u'*Thermistor*', u'PIN?ARRAY*', u'bornier*', u'*Terminal?Block*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermistor_NTC_4wire',dest=TEMPLATE,tool=SKIDL,keywords=u'thermistor NTC resistor sensor RTD',description=u'temperature dependent resistor, negative temperature coefficient (NTC), 4-wire interface',ref_prefix=u'TH',num_units=1,fplist=[u'*NTC*', u'*Thermistor*', u'PIN?ARRAY*', u'bornier*', u'*Terminal?Block*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermistor_PTC',dest=TEMPLATE,tool=SKIDL,keywords=u'resistor PTC thermistor sensor RTD',description=u'temperature dependent resistor, positive temperature coefficient (PTC)',ref_prefix=u'TH',num_units=1,fplist=[u'*PTC*', u'*Thermistor*', u'PIN?ARRAY*', u'bornier*', u'*Terminal?Block*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermistor_PTC_3wire',dest=TEMPLATE,tool=SKIDL,keywords=u'resistor PTC thermistor sensor RTD',description=u'temperature dependent resistor, positive temperature coefficient (PTC), 3-wire interface',ref_prefix=u'TH',num_units=1,fplist=[u'PIN_ARRAY_3X1', u'bornier3', u'TerminalBlock*3pol'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermistor_PTC_4wire',dest=TEMPLATE,tool=SKIDL,keywords=u'resistor PTC thermistor sensor RTD',description=u'temperature dependent resistor, positive temperature coefficient (PTC), 3-wire interface',ref_prefix=u'TH',num_units=1,fplist=[u'PIN_ARRAY_4X1', u'bornier4', u'TerminalBlock*4pol'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermocouple',dest=TEMPLATE,tool=SKIDL,keywords=u'thermocouple temperature sensor cold junction',description=u'thermocouple',ref_prefix=u'TC',num_units=1,fplist=[u'PIN?ARRAY*', u'bornier*', u'*Terminal?Block*', u'Thermo*Couple*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'+',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'-',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermocouple_ALT',dest=TEMPLATE,tool=SKIDL,keywords=u'thermocouple temperature sensor cold junction',description=u'thermocouple with connector block',ref_prefix=u'TC',num_units=1,fplist=[u'PIN?ARRAY*', u'bornier*', u'*Terminal?Block*', u'Thermo*Couple*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'+',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'-',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Thermocouple_Block',dest=TEMPLATE,tool=SKIDL,keywords=u'thermocouple temperature sensor cold junction',description=u'thermocouple with isothermal block',ref_prefix=u'TC',num_units=1,fplist=[u'PIN?ARRAY*', u'bornier*', u'*Terminal?Block*', u'Thermo*Couple*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'+',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'-',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Transformer_1P_1S',dest=TEMPLATE,tool=SKIDL,keywords=u'transformer coil magnet',description=u'Transformer, single primary, single secondary',ref_prefix=u'T',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'AA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'AB',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'SA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'SB',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Transformer_1P_1S_SO8',dest=TEMPLATE,tool=SKIDL,keywords=u'transformer coil magnet',description=u'Transformer, single primary, single secondary, SO-8 package',ref_prefix=u'T',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'AA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'AB',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'SA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'8',name=u'SB',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Transformer_1P_2S',dest=TEMPLATE,tool=SKIDL,keywords=u'transformer coil magnet',description=u'Transformer, single primary, dual secondary',ref_prefix=u'T',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'AA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'AB',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'SA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'SB',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'SC',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'SD',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Transformer_1P_SS',dest=TEMPLATE,tool=SKIDL,keywords=u'transformer coil magnet',description=u'Transformer, single primary, split secondary',ref_prefix=u'T',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'AA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'AB',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'SA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'SC',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'SB',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Transformer_AUDIO',dest=TEMPLATE,tool=SKIDL,keywords=u'transformer coil magnet sound',description=u'Audio transformer',ref_prefix=u'T',num_units=1,do_erc=True,pins=[
            Pin(num=u'0',name=u'~',do_erc=True),
            Pin(num=u'1',name=u'AA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'AB',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'SA',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'SB',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Transformer_SP_1S',dest=TEMPLATE,tool=SKIDL,keywords=u'transformer coil magnet',description=u'Transformer, split primary, single secondary',ref_prefix=u'T',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'PR1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'PM',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'PR2',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'S1',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'S2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Transformer_SP_2S',dest=TEMPLATE,tool=SKIDL,keywords=u'transformer coil magnet',description=u'Transformer, split primary, dual secondary',ref_prefix=u'T',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'IN+',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'PM',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'IN-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'4',name=u'OUT1A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'5',name=u'OUT1B',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'6',name=u'OUT2A',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'7',name=u'OUT2B',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Varistor',dest=TEMPLATE,tool=SKIDL,keywords=u'vdr resistance',description=u'Voltage dependent resistor',ref_prefix=u'RV',num_units=1,fplist=[u'RV_*', u'Varistor*'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Voltage_Divider',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network voltage divider',description=u'voltage divider in a single package',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*', u'SOT?23'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Voltage_Divider_CenterPin1',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network voltage divider',description=u'Voltage Divider (center=pin1)',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*', u'SOT?23'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Voltage_Divider_CenterPin3',dest=TEMPLATE,tool=SKIDL,keywords=u'R Network voltage divider',description=u'Voltage Divider (center=pin3)',ref_prefix=u'RN',num_units=1,fplist=[u'R?Array?SIP*', u'SOT?23'],do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'3',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Voltmeter_AC',dest=TEMPLATE,tool=SKIDL,keywords=u'Voltmeter AC',description=u'AC Voltmeter',ref_prefix=u'MES',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'~',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'~',func=Pin.PASSIVE,do_erc=True)]),
        Part(name=u'Voltmeter_DC',dest=TEMPLATE,tool=SKIDL,keywords=u'Voltmeter DC',description=u'DC Voltmeter',ref_prefix=u'MES',num_units=1,do_erc=True,pins=[
            Pin(num=u'1',name=u'-',func=Pin.PASSIVE,do_erc=True),
            Pin(num=u'2',name=u'+',func=Pin.PASSIVE,do_erc=True)])])