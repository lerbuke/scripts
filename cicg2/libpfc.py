#! python3
import os, sys
from datetime import datetime
import time

class Pfc:
    def __init__(self, name, id, fw):

        self.fd = open(name+'.xml', "w")

        self.av = 0 # analog value instance
        self.mv = 0 # multiple value instance
        self.bv = 0 # binary value instance
        self.nc = 0 # notification class instance
        utc = datetime.utcnow();

        self.fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.fd.write('<wagoDevice deviceType="750-8212" firmwareIndex="{}" copyright="" formatVersion="0.4" creationTool="WagoCfgEngine" '.format(fw))
        self.fd.write('creationDateTime="{}+{:02d}:00" '.format(utc.strftime('%Y-%m-%dT%H:%M:%S'), int(-time.timezone/3600)))
        self.fd.write('creationUtcDateTime="{}" '.format(utc.strftime('%Y-%m-%dT%H:%M:%S')))
        self.fd.write('userVersion="" userID="" userComment="" persistency="1">\n')
        self.fd.write('  <objLst>\n')
        self.fd.write('<obj id="02{0:06x}">\n'.format(id))# 02+ID EN EXA SUR 6 DIGITS (02 03A9E0)
        self.fd.write('<p id="77">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(name))
        self.fd.write('</p>\n')
        self.fd.write('<p id="70" />\n')
        self.fd.write('<p id="44" />\n')
        self.fd.write('<p id="28" s="1" />\n')
        self.fd.write('<p id="339" />\n')
        self.fd.write('<p id="341" />\n')
        self.fd.write('<p id="338" />\n')
        self.fd.write('<p id="340" />\n')
        self.fd.write('</obj>')

    def create_analog_value(self, codesys_name, bacnet_name, desc, unit, min, max, increment):
        if bacnet_name == '' :
            bacnet_name = codesys_name

        self.fd.write('<obj id="0080{0:04x}" cds="1" fbinst="{1}">\n'.format(self.av, codesys_name))  #0080+NO_INSTANCE_AV en HEXA SUR 4 DIGITS   NOM VARIABLE CODESYS
        self.fd.write('<p id="77">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(bacnet_name))   # NOM VARIABLE BACNET
        self.fd.write('</p>\n')
        self.fd.write('<p id="117" s="1">\n')
        self.fd.write('<n t="144" v="{}" />\n'.format(unit)) # 98=UNITE
        self.fd.write('</p>\n')
        self.fd.write('<p id="22" s="1">\n')
        self.fd.write('<n t="64" v="{}" />\n'.format(increment))  # 1=COV INCREMENT
        self.fd.write('</p>\n')
        self.fd.write('<p id="28" s="1">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(desc)) # myDesc=DESCRIPTION
        self.fd.write('</p>\n')
        self.fd.write('<p id="65">\n')
        self.fd.write('<n t="64" v="{}" />\n'.format(max)) # 100=MAX VALUE
        self.fd.write('</p>\n')
        self.fd.write('<p id="69">\n')
        self.fd.write('<n t="64" v="{}" />\n'.format(min)) # 0=MIN VALUE
        self.fd.write('</p>\n')
        self.fd.write('</obj>\n')
        self.av = self.av + 1

    def create_analog_value_array(self, nb, start, codesys_name, bacnet_name, desc, unit, min, max, increment):
        if bacnet_name == '' :
            bacnet_name = codesys_name

        current = start
        for i in range(0, nb):
            self.create_analog_value(codesys_name+'[{}]'.format(current), bacnet_name+'{}'.format(current), desc+ ' {}'.format(current), unit, min, max, increment)
            current = current + 1

    def create_multiple_value(self, codesys_name, bacnet_name, desc, states):
        if bacnet_name == '' :
            bacnet_name = codesys_name

        self.fd.write('<obj id="04C0{0:04x}" cds="1" fbinst="{1}">\n'.format(self.mv, codesys_name)) #  04C0+NO_INSTANCE_MV en HEXA SUR 4 DIGITS NOM VARIABLE CODESYS
        self.fd.write('<p id="77">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(bacnet_name)) # NOM VARIABLE BACNET
        self.fd.write('</p>\n')
        self.fd.write('<p id="74">\n')
        nb = len(states)
        self.fd.write('<n t="32" v="{}" />\n'.format(nb))  # 4 = NOMBRE D'ETAT
        self.fd.write('</p>\n')
        self.fd.write('<p id="28" s="1">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(desc))  # DESCRIPTION
        self.fd.write('</p>\n')
        self.fd.write('<p id="110" s="1">\n')
        for state in states:
            self.fd.write('<n t="112" v="{}" />\n'.format(state)) # DESCRIPTION DES ETATS SELON LE NOMBRE D'ETAT

        self.fd.write('</p>\n')
        self.fd.write('</obj>\n')

        self.mv = self.mv + 1

    def create_multiple_value_array(self, nb, start, codesys_name, bacnet_name, desc, states):#, [desc0, desc1, desc2]):
        if bacnet_name == '' :
            bacnet_name = codesys_name

        current = start
        for i in range(0, nb):
            self.create_multiple_value(codesys_name+'[{}]'.format(current), bacnet_name+'{}'.format(current), desc+ ' {}'.format(current), states)
            current = current + 1

    def create_zone(self, label, desc, modes, types):
        self.create_multiple_value(label + '_MODE', '', 'Mode de fonctionnement ' + desc, modes)

        for type in types:
            self.create_analog_value(label + '_VALEUR_' + type[0], '', desc + ' - Etat courant ' + type , 98, 0, 100, 1)
            self.create_analog_value(label + '_FORCE_' + type[0], '', desc + ' - Valeur de forcage pour ' + type, 98, 0, 100, 1)

    def create_binary_value(self, codesys_name, bacnet_name, desc):
        if bacnet_name == '' :
            bacnet_name = codesys_name

        self.fd.write('<obj id="014{0:05x}" cds="1" fbinst="{1}">\n'.format(self.bv, codesys_name))  # 014 + INSTANCE ID SUR 5 DIGITS EN HEXA
        self.fd.write('<p id="77">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(bacnet_name))
        self.fd.write('</p>\n')
        self.fd.write('<p id="28" s="1">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(desc))
        self.fd.write('</p>\n')
        self.fd.write('</obj>\n')

        self.bv = self.bv + 1

    def create_binary_value_alarm(self, codesys_name, bacnet_name, desc, notification_class, alarm_texts):
        if bacnet_name == '' :
            bacnet_name = codesys_name

        self.fd.write('<obj id="014{0:05x}" cds="1" fbinst="{1}">\n'.format(self.bv, codesys_name))  # 014 + INSTANCE ID SUR 5 DIGITS EN HEXA
        self.fd.write('<p id="75">\n')
        self.fd.write('<n t="192" v="014{0:05x}" />\n'.format(self.bv))
        self.fd.write('</p>\n')
        self.fd.write('<p id="77">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(codesys_name))
        self.fd.write('</p>\n')
        self.fd.write('<p id="28" s="1">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(desc))
        self.fd.write('</p>\n')
        self.fd.write('<p id="6" s="1" />\n')
        self.fd.write('<p id="0" />\n')
        self.fd.write('<p id="354" s="1" />\n')
        self.fd.write('<p id="355" s="1" />\n')
        self.fd.write('<p id="353" s="1" />\n')
        self.fd.write('<p id="35" s="1" />\n')
        self.fd.write('<p id="130" s="0" />\n')
        self.fd.write('<p id="17" s="1">\n')
        self.fd.write('<n t="32" v="{}" />\n'.format(notification_class))
        self.fd.write('</p>\n')
        self.fd.write('<p id="72" s="1" />\n')
        self.fd.write('<p id="113" s="1" />\n')
        self.fd.write('<p id="356" s="1" />\n')
        self.fd.write('<p id="351" s="0" />\n')
        self.fd.write('<p id="352" s="1">\n')
        for alarm in alarm_texts:
            self.fd.write('<n t="112" v="{}" />\n'.format(alarm))
        self.fd.write('</p>\n')
        self.fd.write('</obj>\n')

        self.bv = self.bv + 1

    def create_notification_class(self, name, desc, priorities, acks):
        self.fd.write('<obj id="03C{0:05x}">\n'.format(self.nc)) # 03C +  INSTANCE ID SUR 5 DIGITS EN HEXA
        self.fd.write('<p id="77">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(name))
        self.fd.write('</p>\n')
        self.fd.write('<p id="17">\n')
        self.fd.write('<n t="32" v="{}" />\n'.format(self.nc)) # INSTANCE ID ATTENTION PAS EN HEXA MAIS EN DECIMAL
        self.fd.write('</p>\n')
        self.fd.write('<p id="86" s="1">\n')
        for priority in priorities:
            self.fd.write('<n t="32" v="{}" />\n'.format(priority))
        self.fd.write('</p>\n')
        self.fd.write('<p id="1" s="1">\n')
        self.fd.write('<n t="128" v="{}" />\n'.format(''.join(str(e) for e in acks)))
        self.fd.write('</p>\n')
        self.fd.write('<p id="28" s="1">\n')
        self.fd.write('<n t="112" v="{}" />\n'.format(desc))
        self.fd.write('</p>\n')
        self.fd.write('<p id="102" s="1">\n')
        self.fd.write('<n t="270">\n')
        self.fd.write('<n t="128" v="1111111" />\n')
        self.fd.write('<n t="176" v="00:00:00.00" />\n')
        self.fd.write('<n t="176" v="23:59:59.99" />\n')
        self.fd.write('<n t="268">\n')
        self.fd.write('<n t="192" v="022F6F6D" />\n')
        self.fd.write('</n>\n')
        self.fd.write('<n t="32" v="0" />\n')
        self.fd.write('<n t="16" v="1" />\n')
        self.fd.write('<n t="128" v="111" />\n')
        self.fd.write('</n>\n')
        self.fd.write('</p>\n')
        self.fd.write('</obj>\n')

        self.nc = self.nc + 1

    def end(self):
        self.fd.write('  </objLst>\n')
        self.fd.write('  <cliMapSet />\n')
        self.fd.write('  <objNameMap />\n')
        self.fd.write('  <ptp />\n')
        self.fd.write('  <MultiControllerSettings />\n')
        self.fd.write('</wagoDevice>\n')
        self.fd.close()
