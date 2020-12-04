#!/usr/bin/env python
"""

"""
import os, sys
from datetime import datetime, timezone

class Pfc:
    av = 0
    nv = 0
    
    def __init__(self, name, id, fw):
        
        self.fd = open(name+'.xml', "w")
       

        self.av = 0
        self.mv = 0
        utc = datetime.utcnow();
        
        #print(utc.strftime('%Y-%m-%dT%H:%M:%S%Z'))
        self.fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.fd.write('<wagoDevice deviceType="750-8212" firmwareIndex="{}" copyright="" formatVersion="0.4" creationTool="WagoCfgEngine" creationDateTime="2020-12-03T19:35:48+01:00" creationUtcDateTime="{}" userVersion="" userID="" userComment="" persistency="1">\n'.format(fw, utc.strftime('%Y-%m-%dT%H:%M:%S')))
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
        self.fd.write('<n t="112" v="{}" />\n'.format(desc)) # myDesc=DESRCIPTION
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
        self.fd.write('<n t="112" v="{}" />\n'.format(desc))  # DESCIPTION
        self.fd.write('</p>\n')
        self.fd.write('<p id="110" s="1">\n')
        for state in states:
            self.fd.write('<n t="112" v="{}" />\n'.format(state)) # DESCITPION DES ETATS SELON LE NOMBRE D'ETAT
            
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
    
    
    def end(self):
        self.fd.write('  </objLst>\n')
        self.fd.write('  <cliMapSet />\n')
        self.fd.write('  <objNameMap />\n')
        self.fd.write('  <ptp />\n')
        self.fd.write('  <MultiControllerSettings />\n')
        self.fd.write('</wagoDevice>\n')
        self.fd.close()
  